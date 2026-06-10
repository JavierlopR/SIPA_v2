# Capítulo 3: Arquitectura Propuesta

## 3.1 Visión General del Sistema

### 3.1.1 Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    SIPA v2 Core System                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Data      │  │   Models    │  │   Orchestration     │ │
│  │   Pipeline  │  │   Layer     │  │   & Guardrails      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Market    │  │   User      │  │   Conversational    │ │
│  │   Data      │  │   Behavior  │  │   Interface         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3.1.2 Flujo de Datos Principal

```python
# Pipeline de datos multimodal
class SIPAPipeline:
    def __init__(self):
        self.market_processor = MarketDataProcessor()
        self.behavior_analyzer = UserBehaviorAnalyzer()
        self.bias_detector = CognitiveBiasDetector()
        self.portfolio_optimizer = DeepRLPortfolioOptimizer()
        
    async def process_multimodal_input(self, market_data, user_data, text_input):
        # 1. Procesamiento paralelo de datos
        market_features = await self.market_processor.extract_features(market_data)
        behavior_features = await self.behavior_analyzer.analyze(user_data)
        bias_scores = await self.bias_detector.detect(text_input)
        
        # 2. Fusión de características
        combined_features = self.fuse_features(
            market_features, behavior_features, bias_scores)
        
        # 3. Optimización de cartera
        portfolio_allocation = await self.portfolio_optimizer.optimize(
            combined_features)
        
        # 4. Generación de explicación
        explanation = await self.generate_explanation(
            portfolio_allocation, bias_scores)
            
        return portfolio_allocation, explanation
```

## 3.2 Predictor de Volatilidad con Bi-LSTM

### 3.2.1 Fundamento Teórico

**Motivación Bi-LSTM:**
- **Bidireccionalidad**: Captura dependencias temporales forward y backward
- **Memoria larga**: Resuelve problema de gradientes en RNN tradicionales
- **No-linealidad**: Modela relaciones complejas en volatilidad

**Ventajas sobre GARCH:**
```python
# Comparación conceptual
class GARCHModel:
    """Modelo GARCH tradicional"""
    def __init__(self, p=1, q=1):
        self.p = p  # ARCH terms
        self.q = q  # GARCH terms
        # Supuesto: varianza condicional sigue proceso específico
        
class BiLSTMVolatility:
    """Modelo Bi-LSTM propuesto"""
    def __init__(self, hidden_size=128, num_layers=2):
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        # Ventaja: aprendizaje automático de patrones temporales
```

### 3.2.2 Arquitectura del Modelo

```python
class BiLSTMVolatilityPredictor(nn.Module):
    def __init__(self, input_size=10, hidden_size=128, num_layers=3, dropout=0.2):
        super().__init__()
        
        # Capa Bi-LSTM
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Capas de atención
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_size * 2,
            num_heads=8,
            dropout=dropout
        )
        
        # Capas fully connected
        self.fc1 = nn.Linear(hidden_size * 2, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, 1)  # Output: volatilidad
        
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # x: (batch_size, sequence_length, input_size)
        
        # Bi-LSTM forward pass
        lstm_out, _ = self.lstm(x)
        # lstm_out: (batch_size, sequence_length, hidden_size * 2)
        
        # Self-attention
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        
        # Global average pooling
        pooled = torch.mean(attn_out, dim=1)
        
        # Fully connected layers
        out = self.relu(self.fc1(pooled))
        out = self.dropout(out)
        out = self.relu(self.fc2(out))
        out = self.dropout(out)
        out = self.fc3(out)
        
        return torch.abs(out)  # Volatilidad siempre positiva
```

### 3.2.3 Características de Entrada

```python
class FeatureExtractor:
    def __init__(self):
        self.technical_indicators = [
            'RSI', 'MACD', 'BB_width', 'ATR',  # Volatilidad histórica
            'Volume_ratio', 'Price_momentum',   # Momentum
            'VIX', 'TED_spread', 'Oil_price'    # Factores macro
        ]
    
    def extract_features(self, market_data):
        features = {}
        
        # Indicadores técnicos
        features['rsi'] = self.calculate_rsi(market_data['close'])
        features['macd'] = self.calculate_macd(market_data['close'])
        features['bb_width'] = self.calculate_bollinger_width(market_data['close'])
        features['atr'] = self.calculate_atr(market_data)
        
        # Momentum y volumen
        features['volume_ratio'] = market_data['volume'] / market_data['volume'].rolling(20).mean()
        features['price_momentum'] = market_data['close'].pct_change(5)
        
        # Factores macro (si disponibles)
        if 'vix' in market_data.columns:
            features['vix'] = market_data['vix']
        
        return pd.DataFrame(features)
```

### 3.2.4 Entrenamiento y Validación

```python
class VolatilityTrainer:
    def __init__(self, model, device='cuda'):
        self.model = model.to(device)
        self.device = device
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=10)
        
    def train_epoch(self, train_loader):
        self.model.train()
        total_loss = 0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
            
            self.optimizer.zero_grad()
            predictions = self.model(batch_x)
            loss = self.criterion(predictions, batch_y)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def validate(self, val_loader):
        self.model.eval()
        total_loss = 0
        predictions = []
        actuals = []
        
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                pred = self.model(batch_x)
                loss = self.criterion(pred, batch_y)
                
                total_loss += loss.item()
                predictions.extend(pred.cpu().numpy())
                actuals.extend(batch_y.cpu().numpy())
        
        # Métricas adicionales
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        mse = mean_squared_error(actuals, predictions)
        mae = mean_absolute_error(actuals, predictions)
        r2 = r2_score(actuals, predictions)
        
        return {
            'loss': total_loss / len(val_loader),
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'predictions': predictions,
            'actuals': actuals
        }
```

## 3.3 Detector de Anomalías con VAE

### 3.3.1 Fundamento Teórico

**Variational Autoencoders (VAE):**
- **Aprendizaje no supervisado**: No requiere etiquetas de anomalías
- **Distribución latente**: Aprende representación probabilística
- **Reconstrucción**: Anomalías tienen alto error de reconstrucción

**Aplicación en finanzas:**
```python
# Detección de anomalías en mercado
class FinancialAnomalyDetector:
    """
    Detecta anomalías en:
    - Patrones de precios anómalos
    - Comportamiento de volumen inusual
    - Movimientos de correlación atípicos
    """
```

### 3.3.2 Arquitectura VAE

```python
class FinancialVAE(nn.Module):
    def __init__(self, input_dim=20, latent_dim=8, hidden_dims=[64, 32]):
        super().__init__()
        
        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(0.1)
            ])
            prev_dim = hidden_dim
        
        self.encoder = nn.Sequential(*encoder_layers)
        
        # Capas de distribución latente
        self.fc_mu = nn.Linear(prev_dim, latent_dim)
        self.fc_logvar = nn.Linear(prev_dim, latent_dim)
        
        # Decoder
        decoder_layers = []
        prev_dim = latent_dim
        for hidden_dim in reversed(hidden_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(0.1)
            ])
            prev_dim = hidden_dim
        
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        self.decoder = nn.Sequential(*decoder_layers)
        
    def encode(self, x):
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_logvar(h)
    
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z):
        return self.decoder(z)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
    
    def loss_function(self, recon_x, x, mu, logvar, beta=1.0):
        # Reconstruction loss
        recon_loss = F.mse_loss(recon_x, x, reduction='sum')
        
        # KL divergence
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        
        return recon_loss + beta * kl_loss
```

### 3.3.3 Detección de Anomalías

```python
class AnomalyDetectionSystem:
    def __init__(self, vae_model, threshold_percentile=95):
        self.vae = vae_model
        self.threshold_percentile = threshold_percentile
        self.reconstruction_errors = []
        
    def calculate_reconstruction_error(self, data):
        self.vae.eval()
        with torch.no_grad():
            data_tensor = torch.FloatTensor(data)
            reconstructed, mu, logvar = self.vae(data_tensor)
            
            # Error de reconstrucción por muestra
            errors = F.mse_loss(reconstructed, data_tensor, reduction='none')
            sample_errors = errors.mean(dim=1)
            
            return sample_errors.numpy()
    
    def fit_threshold(self, normal_data):
        """Calcular threshold usando datos normales"""
        errors = self.calculate_reconstruction_error(normal_data)
        self.threshold = np.percentile(errors, self.threshold_percentile)
        self.reconstruction_errors = errors
        
    def detect_anomalies(self, new_data):
        """Detectar anomalías en nuevos datos"""
        errors = self.calculate_reconstruction_error(new_data)
        anomalies = errors > self.threshold
        
        return {
            'is_anomaly': anomalies,
            'reconstruction_errors': errors,
            'anomaly_scores': errors / self.threshold,  # Normalizado
            'threshold': self.threshold
        }
    
    def explain_anomaly(self, anomalous_sample, normal_samples):
        """Explicar por qué una muestra es anómala"""
        # Reconstrucción de muestra anómala
        anomalous_tensor = torch.FloatTensor(anomalous_sample).unsqueeze(0)
        reconstructed_anomalous, _, _ = self.vae(anomalous_tensor)
        
        # Reconstrucción promedio de muestras normales
        normal_tensor = torch.FloatTensor(normal_samples)
        reconstructed_normal, _, _ = self.vae(normal_tensor)
        normal_reconstruction_mean = reconstructed_normal.mean(dim=0)
        
        # Diferencias por feature
        feature_diff = np.abs(
            anomalous_sample - reconstructed_anomalous.squeeze().numpy()
        )
        normal_diff = np.abs(
            normal_samples.mean(axis=0) - normal_reconstruction_mean.numpy()
        )
        
        # Features más anómalas
        anomaly_contribution = feature_diff - normal_diff
        
        return {
            'feature_contributions': anomaly_contribution,
            'top_anomalous_features': np.argsort(anomaly_contribution)[-5:],
            'reconstruction_error': feature_diff.mean()
        }
```

## 3.4 Clasificador de Sesgos Cognitivos con Transformer

### 3.4.1 Sesgos a Detectar

```python
COGNITIVE_BIASES = {
    'overconfidence': {
        'keywords': ['seguro', 'garantizado', 'sin duda', 'claro', 'obvio'],
        'patterns': ['es obvio que', 'estoy seguro de que', 'sin lugar a dudas'],
        'linguistic_markers': ['adverbs_certainty', 'superlatives', 'absolutes']
    },
    'loss_aversion': {
        'keywords': ['perder', 'miedo', 'riesgo', 'peligro', 'evitar'],
        'patterns': ['no quiero perder', 'miedo a', 'es muy arriesgado'],
        'linguistic_markers': ['negativity_bias', 'risk_words', 'avoidance_language']
    },
    'herding': {
        'keywords': ['todos', 'mayoría', 'popular', 'tendencia', 'siguiendo'],
        'patterns': ['todos están', 'la mayoría cree', 'siguiendo la tendencia'],
        'linguistic_markers': ['social_proof', 'conformity', 'popularity_words']
    },
    'anchoring': {
        'keywords': ['inicialmente', 'primera', 'base', 'referencia', 'partir de'],
        'patterns': ['basado en', 'partiendo de', 'mi primera idea'],
        'linguistic_markers': ['reference_points', 'initial_values', 'baseline_language']
    },
    'recency_bias':        'keywords': ['reciente', 'último', 'ahora', 'hoy', 'ayer'],
        'patterns': ['últimamente', 'en los últimos días', 'recientemente'],
        'linguistic_markers': ['temporal_proximity', 'recent_events', 'immediate_focus']
    },
    'confirmation_bias': {
        'keywords': ['confirma', 'demuestra', 'prueba', 'evidencia', 'cierto'],
        'patterns': ['como esperaba', 'confirma que', 'demuestra mi punto'],
        'linguistic_markers': ['confirmatory_evidence', 'selective_attention', 'biased_search']
    }
}
```

### 3.4.2 Arquitectura del Clasificador

```python
class CognitiveBiasClassifier(nn.Module):
    def __init__(self, 
                 model_name='bert-base-uncased',
                 num_labels=len(COGNITIVE_BIASES),
                 hidden_dropout_prob=0.1):
        super().__init__()
        
        # Transformer base
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(hidden_dropout_prob)
        
        # Capa de clasificación multi-label
        self.classifier = nn.Linear(
            self.bert.config.hidden_size, 
            num_labels
        )
        
        # Binary classification para cada sesgo
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, input_ids, attention_mask):
        # BERT forward pass
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Usar [CLS] token para clasificación
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        
        # Clasificación multi-label
        logits = self.classifier(pooled_output)
        probabilities = self.sigmoid(logits)
        
        return {
            'logits': logits,
            'probabilities': probabilities
        }
```

### 3.4.3 Dataset y Preprocesamiento

```python
class CognitiveBiasDataset(Dataset):
    def __init__(self, texts, bias_labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = bias_labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        labels = self.labels[idx]
        
        # Tokenización
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.FloatTensor(labels)
        }

class BiasDataPreprocessor:
    def __init__(self):
        self.patterns = COGNITIVE_BIASES
        self.spacy_model = spacy.load("en_core_web_sm")
        
    def extract_linguistic_features(self, text):
        doc = self.spacy_model(text)
        
        features = {
            'sentiment': self._get_sentiment(text),
            'certainty_score': self._calculate_certainty(doc),
            'risk_words_count': self._count_risk_words(doc),
            'social_proof_words': self._count_social_proof(doc),
            'temporal_focus': self._analyze_temporal_focus(doc),
            'negativity_ratio': self._calculate_negativity_ratio(doc)
        }
        
        return features
    
    def generate_synthetic_training_data(self, base_texts, num_samples=1000):
        """Generar datos de entrenamiento sintéticos"""
        synthetic_data = []
        
        for bias_type, bias_info in COGNITIVE_BIASES.items():
            for _ in range(num_samples // len(COGNITIVE_BIASES)):
                base_text = random.choice(base_texts)
                biased_text = self._inject_bias(base_text, bias_type, bias_info)
                
                labels = [0] * len(COGNITIVE_BIASES)
                labels[list(COGNITIVE_BIASES.keys()).index(bias_type)] = 1
                
                synthetic_data.append({
                    'text': biased_text,
                    'labels': labels,
                    'bias_type': bias_type
                })
        
        return synthetic_data
    
    def _inject_bias(self, text, bias_type, bias_info):
        """Inyectar sesgo específico en texto"""
        # Implementación de inyección de sesgos
        modifiers = bias_info['patterns']
        replacement = random.choice(modifiers)
        
        # Estrategias de inyección según tipo de sesgo
        if bias_type == 'overconfidence':
            return f"{replacement} que {text.lower()}"
        elif bias_type == 'loss_aversion':
            return f"Tengo {replacement} perder dinero si {text.lower()}"
        # ... más estrategias
        
        return text
```

### 3.4.4 Entrenamiento y Evaluación

```python
class BiasClassifierTrainer:
    def __init__(self, model, device='cuda'):
        self.model = model.to(device)
        self.device = device
        
        # Loss function para multi-label classification
        self.criterion = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
        
        # Métricas específicas para detección de sesgos
        self.metrics = {
            'precision': MultilabelPrecision(),
            'recall': MultilabelRecall(),
            'f1': MultilabelF1Score()
        }
    
    def train_epoch(self, train_loader):
        self.model.train()
        total_loss = 0
        
        for batch in train_loader:
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            self.optimizer.zero_grad()
            
            outputs = self.model(input_ids, attention_mask)
            loss = self.criterion(outputs['logits'], labels)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def evaluate(self, val_loader):
        self.model.eval()
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(input_ids, attention_mask)
                predictions = (outputs['probabilities'] > 0.5).float()
                
                all_predictions.append(predictions.cpu())
                all_labels.append(labels.cpu())
        
        all_predictions = torch.cat(all_predictions, dim=0)
        all_labels = torch.cat(all_labels, dim=0)
        
        # Calcular métricas por bias
        results = {}
        bias_names = list(COGNITIVE_BIASES.keys())
        
        for i, bias_name in enumerate(bias_names):
            pred_bias = all_predictions[:, i]
            true_bias = all_labels[:, i]
            
            results[bias_name] = {
                'precision': precision_score(true_bias, pred_bias),
                'recall': recall_score(true_bias, pred_bias),
                'f1': f1_score(true_bias, pred_bias),
                'support': true_bias.sum().item()
            }
        
        return results
```

## 3.5 Sistema Conversacional con LLM + RAG

### 3.5.1 Arquitectura RAG (Retrieval-Augmented Generation)

```python
class SIPAConversationalSystem:
    def __init__(self):
        # Componentes RAG
        self.vector_store = FinancialKnowledgeBase()
        self.retriever = DocumentRetriever(self.vector_store)
        self.generator = LLMGenerator()
        
        # Componentes específicos de SIPA
        self.bias_detector = CognitiveBiasDetector()
        self.portfolio_analyzer = PortfolioAnalyzer()
        self.explanation_generator = ExplanationGenerator()
        
    async def process_user_query(self, query, user_context):
        # 1. Detección de sesgos en la consulta
        bias_analysis = await self.bias_detector.analyze(query)
        
        # 2. Recuperación de información relevante
        relevant_docs = await self.retriever.retrieve(
            query, k=5, user_profile=user_context
        )
        
        # 3. Análisis de cartera si aplica
        portfolio_context = None
        if self._is_portfolio_query(query):
            portfolio_context = await self.portfolio_analyzer.analyze(
                user_context['portfolio']
            )
        
        # 4. Generación de respuesta con contexto
        response = await self.generator.generate_response(
            query=query,
            retrieved_docs=relevant_docs,
            bias_analysis=bias_analysis,
            portfolio_context=portfolio_context,
            user_context=user_context
        )
        
        # 5. Post-procesamiento y validación
        final_response = await self._validate_and_enhance_response(
            response, bias_analysis
        )
        
        return final_response
```

### 3.5.2 Base de Conocimiento Financiera

```python
class FinancialKnowledgeBase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        
    def build_knowledge_base(self, documents):
        """Construir base de conocimiento financiera"""
        
        # Fuentes de conocimiento
        knowledge_sources = {
            'academic_papers': self._load_academic_papers(),
            'market_analysis': self._load_market_analysis(),
            'behavioral_finance': self._load_behavioral_finance(),
            'risk_management': self._load_risk_management(),
            'portfolio_theory': self._load_portfolio_theory(),
            'regulations': self._load_regulations()
        }
        
        all_chunks = []
        for source_type, docs in knowledge_sources.items():
            chunks = self.text_splitter.split_documents(docs)
            for chunk in chunks:
                chunk.metadata['source_type'] = source_type
            all_chunks.extend(chunks)
        
        # Crear vector store
        self.vector_store = FAISS.from_documents(
            all_chunks, self.embeddings
        )
        
        return self.vector_store
    
    def _load_academic_papers(self):
        """Cargar papers académicos relevantes"""
        papers = [
            "Markowitz Portfolio Theory",
            "Black-Litterman Model",
            "Behavioral Finance Principles",
            "Deep Learning in Finance",
            "Risk Management Frameworks"
        ]
        # Implementar carga real de documentos
        return []
    
    def semantic_search(self, query, k=5, filters=None):
        """Búsqueda semántica en base de conocimiento"""
        if filters:
            # Filtrar por tipo de fuente
            filtered_docs = [
                doc for doc in self.vector_store.similarity_search(query, k=k*2)
                if doc.metadata.get('source_type') in filters
            ]
            return filtered_docs[:k]
        
        return self.vector_store.similarity_search(query, k=k)
```

### 3.5.3 Generador de Explicaciones

```python
class ExplanationGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)
        
    def generate_portfolio_explanation(self, allocation, risk_profile, market_conditions):
        """Generar explicación de allocation de cartera"""
        
        prompt = f"""
        Como asesor financiero experto, explica la siguiente asignación de cartera:
        
        PERFIL DEL INVERSOR: {risk_profile}
        CONDICIONES DE MERCADO: {market_conditions}
        
        ASIGNACIÓN PROPUESTA:
        {self._format_allocation(allocation)}
        
        INSTRUCCIONES:
        1. Explica el razonamiento detrás de cada asignación
        2. Conecta con el perfil de riesgo del inversor
        3. Considera las condiciones actuales del mercado
        4. Usa lenguaje claro y educativo
        5. Incluye advertencias de riesgo apropiadas
        6. Mantén un tono profesional pero accesible
        
        Estructura tu respuesta en:
        - Resumen ejecutivo
        - Detalle por clase de activo
        - Consideraciones de riesgo
        - Recomendaciones de seguimiento
        """
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def generate_bias_explanation(self, detected_biases, user_input):
        """Explicar sesgos detectados al usuario"""
        
        bias_explanations = {
            'overconfidence': "He notado un alto grado de confianza en tu análisis. Esto es común, pero importante equilibrar con humildad intelectual.",
            'loss_aversion': "Percibo una fuerte aversión a pérdidas. Es natural, pero a veces nos hace perder oportunidades.",
            'herding': "Noté que mencionas seguir la tendencia de 'todos'. Es importante pensar independientemente.",
            # ... más explicaciones
        }
        
        prompt = f"""
        El usuario ha dicho: "{user_input}"
        
        He detectado posibles sesgos: {', '.join(detected_biases)}
        
        Genera una respuesta empática que:
        1. Reconozca la validez de su preocupación
        2. Explique suavemente el sesgo detectado
        3. Ofrezca una perspectiva alternativa
        4. Sugerirá una acción constructiva
        
        Tono: educativo, no crítico, empático
        """
        
        return self.llm.invoke(prompt).content
    
    def generate_risk_explanation(self, risk_metrics, portfolio_allocation):
        """Explicar métricas de riesgo"""
        
        prompt = f"""
        Explica las siguientes métricas de riesgo para esta cartera:
        
        MÉTRICAS:
        - VaR 95%: {risk_metrics['var_95']}%
        - Volatilidad anual: {risk_metrics['volatility']}%
        - Sharpe Ratio: {risk_metrics['sharpe']}
        - Max Drawdown: {risk_metrics['max_dd']}%
        
        CARTERA:
        {self._format_allocation(portfolio_allocation)}
        
        Explica cada métrica en términos simples y qué significan para el inversor.
        """
        
        return self.llm.invoke(prompt).content
```

## 3.6 Optimizador de Cartera con Deep RL (PPO)

### 3.6.1 Environment de Trading

```python
class PortfolioEnvironment(gym.Env):
    def __init__(self, 
                 market_data, 
                 initial_balance=100000,
                 transaction_costs=0.001,
                 window_size=60):
        super().__init__()
        
        self.market_data = market_data
        self.initial_balance = initial_balance
        self.transaction_costs = transaction_costs
        self.window_size = window_size
        
        # Espacio de acción: allocation porcentual por activo
        self.n_assets = len(market_data.columns) - 1  # Excluyendo fecha
        self.action_space = spaces.Box(
            low=0, high=1, shape=(self.n_assets,), dtype=np.float32
        )
        
        # Espacio de observación: features de mercado + estado de cartera
        n_features = window_size * self.n_assets + self.n_assets + 3  # + cash, total_value, time
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(n_features,), dtype=np.float32
        )
        
        self.reset()
    
    def reset(self):
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.portfolio = np.zeros(self.n_assets)
        self.portfolio_value = self.initial_balance
        self.transaction_history = []
        
        return self._get_observation()
    
    def step(self, action):
        # Normalizar acción para que sume 1
        action = self._normalize_action(action)
        
        # Ejecutar rebalanceo
        prev_value = self.portfolio_value
        transaction_cost = self._execute_rebalance(action)
        
        # Calcular nueva valoración
        self.portfolio_value = self._calculate_portfolio_value()
        
        # Calcular reward
        reward = self._calculate_reward(prev_value, transaction_cost)
        
        # Avanzar tiempo
        self.current_step += 1
        done = self.current_step >= len(self.market_data) - 1
        
        return self._get_observation(), reward, done, {
            'portfolio_value': self.portfolio_value,
            'transaction_cost': transaction_cost,
            'action': action
        }
    
    def _normalize_action(self, action):
        """Asegurar que las acciones sumen 1"""
        action = np.abs(action)  # No posiciones cortas
        return action / action.sum()
    
    def _execute_rebalance(self, target_allocation):
        """Ejecutar rebalanceo con costos de transacción"""
        # Valor actual por activo
        current_values = self.portfolio * self._get_current_prices()
        target_values = target_allocation * self.portfolio_value
        
        # Cambios necesarios
        changes = target_values - current_values
        transaction_cost = np.abs(changes).sum() * self.transaction_costs
        
        # Actualizar portfolio
        self.portfolio = target_allocation
        self.balance = self.portfolio_value - transaction_cost
        
        self.transaction_history.append({
            'step': self.current_step,
            'allocation': target_allocation.copy(),
            'cost': transaction_cost
        })
        
        return transaction_cost
    
    def _calculate_portfolio_value(self):
        """Calcular valor total de la cartera"""
        prices = self._get_current_prices()
        return np.dot(self.portfolio, prices) + self.balance
    
    def _calculate_reward(self, prev_value, transaction_cost):
        """Función de reward multi-objetivo"""
        # Retorno de la cartera
        portfolio_return = (self.portfolio_value - prev_value) / prev_value
        
        # Penalización por alta volatilidad (si tenemos historial)
        volatility_penalty = 0
        if len(self.transaction_history) > 10:
            recent_returns = [
                h['portfolio_value'] / prev_value - 1
                for h in self.transaction_history[-10:]
            ]
            volatility = np.std(recent_returns)
            volatility_penalty = -0.1 * volatility
        
        # Penalización por costos de transacción
        cost_penalty = -transaction_cost / self.portfolio_value
        
        # Reward total
        reward = portfolio_return + volatility_penalty + cost_penalty
        
        return reward
    
    def _get_observation(self):
        """Construir observación para el agente"""
        # Features de mercado (ventana temporal)
        market_window = self.market_data.iloc[
            self.current_step - self.window_size:self.current_step
        ].values.flatten()
        
        # Estado actual de la cartera
        portfolio_state = np.concatenate([
            self.portfolio,
            [self.balance / self.portfolio_value],
            [self.current_step / len(self.market_data)]
        ])
        
        return np.concatenate([market_window, portfolio_state])
```

### 3.6.2 Agente PPO

```python
class PPOPortfolioOptimizer:
    def __init__(self, 
                 env,
                 learning_rate=3e-4,
                 n_steps=2048,
                 batch_size=64,
                 n_epochs=10,
                 gamma=0.99,
                 gae_lambda=0.95,
                 clip_range=0.2,
                 ent_coef=0.01):
        
        self.env = env
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Red neuronal (Actor-Crítico)
        self.actor_critic = ActorCriticNetwork(
            input_dim=env.observation_space.shape[0],
            output_dim=env.action_space.shape[0]
        ).to(self.device)
        
        # Hiperparámetros PPO
        self.learning_rate = learning_rate
        self.n_steps = n_steps
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_range = clip_range
        self.ent_coef = ent_coef
        
        # Optimizadores
        self.optimizer = torch.optim.Adam(
            self.actor_critic.parameters(), 
            lr=learning_rate
        )
        
        # Storage para trajectories
        self.storage = PPOStorage(
            observation_space=env.observation_space,
            action_space=env.action_space,
            n_steps=n_steps,
            batch_size=batch_size
        )
    
    def learn(self, total_timesteps):
        """Entrenamiento del agente PPO"""
        timestep = 0
        
        while timestep < total_timesteps:
            # Collect trajectories
            obs = self.env.reset()
            
            for step in range(self.n_steps):
                # Action selection
                with torch.no_grad():
                    obs_tensor = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
                    action, value, log_prob = self.actor_critic.act(obs_tensor)
                
                # Environment step
                next_obs, reward, done, info = self.env.step(action.cpu().numpy())
                
                # Store transition
                self.storage.store(
                    obs, action.cpu().numpy(), reward, done, value.cpu().numpy(),
                    log_prob.cpu().numpy()
                )
                
                obs = next_obs
                timestep += 1
                
                if done:
                    obs = self.env.reset()
            
            # Compute advantages
            advantages = self._compute_advantages()
            
            # PPO update
            for epoch in range(self.n_epochs):
                for batch in self.storage.get_batches(advantages):
                    self._update_network(batch)
            
            # Clear storage
            self.storage.clear()
    
    def _compute_advantages(self):
        """Computar Generalized Advantage Estimation (GAE)"""
        advantages = np.zeros(len(self.storage.rewards))
        last_advantage = 0
        
        for t in reversed(range(len(self.storage.rewards))):
            if t == len(self.storage.rewards) - 1:
                next_value = 0
            else:
                next_value = self.storage.values[t + 1]
            
            delta = self.storage.rewards[t] + self.gamma * next_value - self.storage.values[t]
            advantages[t] = delta + self.gamma * self.gae_lambda * last_advantage
            last_advantage = advantages[t]
        
        return advantages
    
    def _update_network(self, batch):
        """Actualización de red con clipping PPO"""
        obs, actions, old_log_probs, advantages, returns = batch
        
        # Convertir a tensores
        obs = torch.FloatTensor(obs).to(self.device)
        actions = torch.FloatTensor(actions).to(self.device)
        old_log_probs = torch.FloatTensor(old_log_probs).to(self.device)
        advantages = torch.FloatTensor(advantages).to(self.device)
        returns = torch.FloatTensor(returns).to(self.device)
        
        # Forward pass
        values, log_probs, entropy = self.actor_critic.evaluate(obs, actions)
        
        # Ratio de probabilidades
        ratio = torch.exp(log_probs - old_log_probs)
        
        # Clipped surrogate objective
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - self.clip_range, 1 + self.clip_range) * advantages
        policy_loss = -torch.min(surr1, surr2).mean()
        
        # Value function loss
        value_loss = F.mse_loss(values.squeeze(), returns)
        
        # Entropy bonus
        entropy_loss = -entropy.mean()
        
        # Total loss
        loss = policy_loss + 0.5 * value_loss + self.ent_coef * entropy_loss
        
        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.actor_critic.parameters(), 0.5)
        self.optimizer.step()
    
    def get_portfolio_allocation(self, observation):
        """Obtener allocation para observación actual"""
        with torch.no_grad():
            obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)
            action, _, _ = self.actor_critic.act(obs_tensor)
            return self._normalize_allocation(action.cpu().numpy())
    
    def _normalize_allocation(self, action):
        """Normalizar allocation para que sume 1"""
        action = np.abs(action)
        return action / action.sum()

class ActorCriticNetwork(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=256):
        super().__init__()
        
        # Shared layers
        self.shared_layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Actor head (policy)
        self.actor_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, output_dim),
            nn.Softmax(dim=-1)
        )
        
        # Critic head (value function)
        self.critic_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )
    
    def forward(self, x):
        shared_features = self.shared_layers(x)
        action_probs = self.actor_head(shared_features)
        value = self.critic_head(shared_features)
        return action_probs, value
    
    def act(self, observation):
        """Selección de acción con exploración"""
        action_probs, value = self.forward(observation)
        dist = torch.distributions.Categorical(action_probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action, value, log_prob
    
    def evaluate(self, observation, action):
        """Evaluación para training"""
        action_probs, value = self.forward(observation)
        dist = torch.distributions.Categorical(action_probs)
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()
        return value, log_prob, entropy
```

## 3.7 Capa de Orquestación y Guardrails

### 3.7.1 Sistema de Orquestación

```python
class SIPAOrchestrator:
    def __init__(self):
        # Componentes del sistema
        self.volatility_predictor = BiLSTMVolatilityPredictor()
        self.anomaly_detector = FinancialAnomalyDetector()
        self.bias_classifier = CognitiveBiasClassifier()
        self.rl_optimizer = PPOPortfolioOptimizer()
        self.conversational_system = SIPAConversationalSystem()
        
        # Guardrails y validación
        self.risk_manager = RiskGuardrails()
        self.compliance_checker = ComplianceChecker()
        self.performance_monitor = PerformanceMonitor()
        
    async def process_user_request(self, request_data):
        """Procesamiento principal de solicitudes de usuario"""
        
        try:
            # 1. Validación inicial
            validation_result = await self._validate_request(request_data)
            if not validation_result['is_valid']:
                return self._format_error_response(validation_result['error'])
            
            # 2. Análisis de comportamiento y sesgos
            bias_analysis = await self._analyze_user_behavior(request_data)
            
            # 3. Evaluación de condiciones de mercado
            market_analysis = await self._analyze_market_conditions(request_data)
            
            # 4. Detección de anomalías
            anomaly_check = await self._check_anomalies(market_analysis)
            
            # 5. Optimización de cartera
            if anomaly_check['has_anomalies']:
                portfolio_allocation = await self._get_safe_allocation()
            else:
                portfolio_allocation = await self._optimize_portfolio(
                    request_data, bias_analysis, market_analysis
                )
            
            # 6. Generación de explicación
            explanation = await self._generate_explanation(
                portfolio_allocation, bias_analysis, market_analysis
            )
            
            # 7. Validación final de guardrails
            final_validation = await self._apply_guardrails(
                portfolio_allocation, explanation
            )
            
            return {
                'status': 'success',
                'portfolio_allocation': final_validation['allocation'],
                'explanation': final_validation['explanation'],
                'risk_metrics': final_validation['risk_metrics'],
                'bias_alerts': bias_analysis['detected_biases'],
                'market_insights': market_analysis['insights']
            }
            
        except Exception as e:
            return await self._handle_system_error(e)
    
    async def _validate_request(self, request_data):
        """Validación inicial de solicitudes"""
        required_fields = ['user_profile', 'portfolio_data', 'risk_tolerance']
        
        for field in required_fields:
            if field not in request_data:
                return {'is_valid': False, 'error': f'Missing field: {field}'}
        
        # Validaciones específicas
        if request_data['risk_tolerance'] not in ['conservative', 'moderate', 'aggressive']:
            return {'is_valid': False, 'error': 'Invalid risk tolerance'}
        
        return {'is_valid': True}
    
    async def _analyze_user_behavior(self, request_data):
        """Análisis de comportamiento y detección de sesgos"""
        
        # Análisis de texto reciente
        text_inputs = request_data.get('recent_interactions', [])
        bias_scores = await self.bias_classifier.analyze_text_batch(text_inputs)
        
        # Análisis de patrones de trading
        trading_patterns = self._analyze_trading_patterns(
            request_data.get('trading_history', [])
        )
        
        # Análisis temporal
        temporal_patterns = self._analyze_temporal_behavior(
            request_data.get('interaction_timestamps', [])
        )
        
        return {
            'detected_biases': bias_scores,
            'trading_patterns': trading_patterns,
            'temporal_patterns': temporal_patterns,
            'risk_adjustment_factor': self._calculate_risk_adjustment(
                bias_scores, trading_patterns
            )
        }
    
    async def _analyze_market_conditions(self, request_data):
        """Análisis de condiciones actuales del mercado"""
        
        # Predicción de volatilidad
        volatility_forecast = await self.volatility_predictor.predict(
            request_data['market_data']
        )
        
        # Análisis de sentimiento de mercado
        sentiment_analysis = await self._analyze_market_sentiment()
        
        # Análisis de correlaciones
        correlation_analysis = self._analyze_correlations(
            request_data['market_data']
        )
        
        return {
            'volatility_forecast': volatility_forecast,
            'sentiment': sentiment_analysis,
            'correlations': correlation_analysis,
            'market_regime': self._classify_market_regime(volatility_forecast, sentiment_analysis),
            'insights': self._generate_market_insights(volatility_forecast, sentiment_analysis)
        }
    
    async def _optimize_portfolio(self, request_data, bias_analysis, market_analysis):
        """Optimización de cartera considerando todos los factores"""
        
        # Ajustar tolerancia al riesgo según sesgos detectados
        adjusted_risk_tolerance = self._adjust_risk_tolerance(
            request_data['risk_tolerance'],
            bias_analysis['risk_adjustment_factor']
        )
        
        # Construir environment para RL
        env = PortfolioEnvironment(
            market_data=request_data['market_data'],
            risk_profile=adjusted_risk_tolerance,
            market_conditions=market_analysis
        )
        
        # Obtener allocation óptima
        allocation = await self.rl_optimizer.get_portfolio_allocation(
            env.get_current_observation()
        )
        
        # Aplicar restricciones de compliance
        compliant_allocation = await self.compliance_checker.validate_allocation(
            allocation, request_data['user_profile']
        )
        
        return compliant_allocation
```

### 3.7.2 Guardrails de Riesgo

```python
class RiskGuardrails:
    def __init__(self):
        self.max_position_size = 0.3  # Máximo 30% en un activo
        self.max_sector_exposure = 0.4  # Máximo 40% en un sector
        self.min_diversification = 5  # Mínimo 5 activos diferentes
        self.max_volatility_target = 0.2  # Máximo 20% volatilidad anual
        
    def validate_allocation(self, allocation, user_profile, market_conditions):
        """Validar allocation contra reglas de riesgo"""
        
        violations = []
        adjusted_allocation = allocation.copy()
        
        # 1. Check tamaño máximo de posición
        max_position = np.max(allocation)
        if max_position > self.max_position_size:
            violations.append(f"Position size {max_position:.2%} exceeds limit {self.max_position_size:.2%}")
            adjusted_allocation = self._reduce_large_positions(adjusted_allocation)
        
        # 2. Check diversificación mínima
        n_positions = np.sum(allocation > 0.01)  # Posiciones > 1%
        if n_positions < self.min_diversification:
            violations.append(f"Insufficient diversification: {n_positions} positions")
            adjusted_allocation = self._increase_diversification(adjusted_allocation)
        
        # 3. Check exposición sectorial
        sector_exposure = self._calculate_sector_exposure(adjusted_allocation)
        for sector, exposure in sector_exposure.items():
            if exposure > self.max_sector_exposure:
                violations.append(f"Sector {sector} exposure {exposure:.2%} exceeds limit")
                adjusted_allocation = self._reduce_sector_exposure(adjusted_allocation, sector)
        
        # 4. Check volatilidad proyectada
        projected_volatility = self._estimate_portfolio_volatility(
            adjusted_allocation, market_conditions
        )
        if projected_volatility > self.max_volatility_target:
            violations.append(f"Projected volatility {projected_volatility:.2%} exceeds target")
            adjusted_allocation = self._reduce_volatility(adjusted_allocation)
        
        # 5. Check consistencia con perfil de usuario
        risk_score = self._calculate_risk_score(adjusted_allocation, market_conditions)
        if not self._is_risk_appropriate(risk_score, user_profile['risk_tolerance']):
            violations.append("Risk level inconsistent with user profile")
            adjusted_allocation = self._adjust_to_risk_profile(
                adjusted_allocation, user_profile['risk_tolerance']
            )
        
        return {
            'is_valid': len(violations) == 0,
            'violations': violations,
            'adjusted_allocation': adjusted_allocation,
            'risk_metrics': {
                'projected_volatility': projected_volatility,
                'risk_score': risk_score,
                'diversification_score': self._calculate_diversification_score(adjusted_allocation)
            }
        }
    
    def _reduce_large_positions(self, allocation):
        """Reducir posiciones grandes que exceden límites"""
        adjusted = allocation.copy()
        
        while np.max(adjusted) > self.max_position_size:
            max_idx = np.argmax(adjusted)
            excess = adjusted[max_idx] - self.max_position_size
            
            # Redistribuir exceso a otras posiciones
            other_indices = [i for i in range(len(adjusted)) if i != max_idx and adjusted[i] > 0]
            if other_indices:
                redistribution = excess / len(other_indices)
                adjusted[max_idx] = self.max_position_size
                for idx in other_indices:
                    adjusted[idx] += redistribution
            else:
                break
        
        return adjusted / adjusted.sum()  # Renormalizar
    
    def _estimate_portfolio_volatility(self, allocation, market_conditions):
        """Estimar volatilidad de la cartera"""
        # Usar pronóstico de volatilidad del Bi-LSTM
        individual_volatilities = market_conditions.get('volatility_forecast', {})
        correlation_matrix = market_conditions.get('correlation_matrix', np.eye(len(allocation)))
        
        # Calcular volatilidad del portfolio
        portfolio_variance = np.dot(allocation, np.dot(correlation_matrix, allocation))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        return portfolio_volatility
```

### 3.7.3 Sistema de Compliance

```python
class ComplianceChecker:
    def __init__(self):
        self.restricted_sectors = ['weapons', 'tobacco', 'gambling']
        self.restricted_countries = [' sanctioned_countries_list']
        self.min_liquidity_requirement = 0.1  # Mínimo 10% en activos líquidos
        
    def validate_allocation(self, allocation, user_profile):
        """Validar allocation contra regulaciones y políticas"""
        
        violations = []
        adjusted_allocation = allocation.copy()
        
        # 1. Check sectores restringidos
        sector_violations = self._check_restricted_sectors(allocation)
        if sector_violations:
            violations.extend(sector_violations)
            adjusted_allocation = self._remove_restricted_sectors(adjusted_allocation)
        
        # 2. Check requerimientos de liquidez
        liquidity_score = self._calculate_liquidity_score(adjusted_allocation)
        if liquidity_score < self.min_liquidity_requirement:
            violations.append(f"Insufficient liquidity: {liquidity_score:.2%}")
            adjusted_allocation = self._increase_liquidity(adjusted_allocation)
        
        # 3. Check perfil de inversor (KYC)
        kyc_compliance = self._check_kyc_compliance(adjusted_allocation, user_profile)
        if not kyc_compliance['is_compliant']:
            violations.extend(kyc_compliance['violations'])
            adjusted_allocation = kyc_compliance['adjusted_allocation']
        
        # 4. Check límites regulatorios
        regulatory_limits = self._check_regulatory_limits(adjusted_allocation, user_profile)
        if not regulatory_limits['is_compliant']:
            violations.extend(regulatory_limits['violations'])
            adjusted_allocation = regulatory_limits['adjusted_allocation']
        
        return adjusted_allocation
    
    def _check_restricted_sectors(self, allocation):
        """Verificar exposición a sectores restringidos"""
        violations = []
        
        # Implementar lógica de verificación de sectores
        # Esto requeriría mapeo de activos a sectores
        
        return violations
    
    def _calculate_liquidity_score(self, allocation):
        """Calcular score de liquidez de la cartera"""
        # Implementar cálculo basado en volumen de trading, bid-ask spreads, etc.
        return 0.8  # Placeholder
    
    def _check_kyc_compliance(self, allocation, user_profile):
        """Verificar compliance con KYC y perfil de inversor"""
        
        # Reglas según perfil de inversor
        profile_rules = {
            'conservative': {
                'max_equity': 0.4,
                'min_fixed_income': 0.6,
                'max_alternatives': 0.0
            },
            'moderate': {
                'max_equity': 0.7,
                'min_fixed_income': 0.3,
                'max_alternatives': 0.1
            },
            'aggressive': {
                'max_equity': 0.9,
                'min_fixed_income': 0.1,
                'max_alternatives': 0.2
            }
        }
        
        user_profile_type = user_profile.get('risk_profile', 'moderate')
        rules = profile_rules[user_profile_type]
        
        violations = []
        
        # Implementar verificación de reglas específicas
        
        return {
            'is_compliant': len(violations) == 0,
            'violations': violations,
            'adjusted_allocation': allocation  # Placeholder
        }
```

Esta arquitectura completa integra todos los componentes necesarios para SIPA v2, desde la predicción de volatilidad hasta la optimización de cartera con Deep RL, todo orquestado con guardrails apropiados para asegurar compliance y gestión de riesgo.
