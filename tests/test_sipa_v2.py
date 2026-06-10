#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test sistemático de SIPA v2 — 11 casos de borde"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from market_analysis import extract_ticker_from_text, get_ticker_audit
from coach import generate_coach_response

test_cases = [
    # (texto, sesgo, ticker_esperado o None)
    ("Compre nvidia y esta cayendo deberia vender?",          "panico",          "NVDA"),
    ("Todos mis amigos ganaron con bitcoin entro ahora?",     "fomo",            "BTC-USD"),
    ("Tengo apple desde hace 3 anos quiero comprar mas",      "ninguno",         "AAPL"),
    ("La compre a 50 no vendo hasta que vuelva a 50 trade republic", "anchoring", None),
    ("Que opinas de ASML para largo plazo?",                  "ninguno",         "ASML.AS"),
    ("Soy muy bueno leyendo charts compre ethereum soporte",  "overconfidence",  "ETH-USD"),
    ("Tengo tesla y baja y baja no puedo dormir",             "loss_aversion",   "TSLA"),
    ("Que diferencia hay entre revolut y ibkr?",              "ninguno",          None),
    ("XYZABC999 deberia comprar?",                            "ninguno",          None),
    ("Quiero meter todo en solana que piensas",               "fomo",            "SOL-USD"),
    ("Tengo santander en openbank debo venderla?",            "ninguno",         "SAN.MC"),
]

print("=== PRUEBA SISTEMATICA SIPA v2 — 11 casos ===\n")
passed = 0
failed = 0
failures = []

for i, (texto, sesgo, ticker_exp) in enumerate(test_cases):
    detected_t = extract_ticker_from_text(texto)

    # Ticker correcto si coincide O si ambos son None
    ticker_ok = (detected_t == ticker_exp)

    audit = get_ticker_audit(detected_t) if detected_t else None

    resp = generate_coach_response(
        user_text=texto,
        detected_intent="consulta",
        detected_bias=sesgo,
        bias_probs={sesgo: 0.80},
        broker_id=None,
        openai_key=None,
        ticker_audit=audit,
    )

    resp_ok = resp.get("success") and len(resp.get("response", "")) > 100

    status = "PASS" if (ticker_ok and resp_ok) else "FAIL"
    if status == "PASS":
        passed += 1
    else:
        failed += 1
        failures.append(
            f"Caso {i+1}: ticker_ok={ticker_ok} ({detected_t} vs {ticker_exp}), resp_ok={resp_ok}"
        )

    # Mostrar resultado
    resp_len = len(resp.get("response", ""))
    print(
        f"  [{i+1:02d}] {status} | "
        f"ticker={detected_t} (exp={ticker_exp}) | "
        f"sesgo={sesgo} | resp_len={resp_len}b"
    )

print()
print(f"RESULTADO FINAL: {passed}/{len(test_cases)} PASS", end="")
if failed:
    print(f" | {failed} FAIL")
    for f in failures:
        print(f"  ⚠ {f}")
else:
    print(" — TODOS LOS CASOS SUPERADOS ✅")
