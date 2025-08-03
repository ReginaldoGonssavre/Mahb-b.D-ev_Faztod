import React, { useState, useRef, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Card, ListGroup, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; // Import the new CSS file

interface ConversationMessage {
  type: 'user' | 'rag';
  content: string;
}

function App() {
  const [documentText, setDocumentText] = useState('');
  const [queryText, setQueryText] = useState('');
  const [conversation, setConversation] = useState<ConversationMessage[]>([]);
  const [uploadedDocuments, setUploadedDocuments] = useState<string[]>([]);
  const [retrievedChunks, setRetrievedChunks] = useState<string[]>([]);
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);

  const chatHistoryRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat history to bottom
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [conversation]);

  const handleDocumentUpload = async () => {
    if (!documentText.trim()) {
      setMessage('Por favor, insira algum texto para o documento.');
      return;
    }
    setIsUploading(true);
    setMessage('');
    try {
      const response = await fetch('http://localhost:8000/upload-document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: documentText }),
      });
      const data = await response.json();
      setMessage(data.message);
      setUploadedDocuments(prev => [...prev, documentText]);
      setDocumentText(''); // Clear textarea after upload
    } catch (error) {
      setMessage('Erro ao carregar documento.');
      console.error('Erro ao carregar documento:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleQueryRag = async () => {
    if (!queryText.trim()) {
      setMessage('Por favor, insira sua pergunta.');
      return;
    }
    const userQuery = queryText;
    setConversation(prev => [...prev, { type: 'user', content: userQuery }]);
    setQueryText(''); // Clear input after sending
    setRetrievedChunks([]); // Clear previous retrieved chunks
    setIsQuerying(true);

    try {
      const response = await fetch('http://localhost:8000/query-rag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery }),
      });
      const data = await response.json();
      setConversation(prev => [...prev, { type: 'rag', content: data.response }]);
      setRetrievedChunks(data.retrieved_chunks);
    } catch (error) {
      setConversation(prev => [...prev, { type: 'rag', content: 'Desculpe, não consegui processar sua pergunta no momento.' }]);
      console.error('Erro ao consultar RAG:', error);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <Container className="mt-5">
      <h1 className="text-center mb-4">Maḥbūb The Ai Software Engineer</h1>

      <Row>
        <Col md={6}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Carregar Documento</Card.Title>
              <Form.Group className="mb-3">
                <Form.Label>Conteúdo do Documento</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={5}
                  value={documentText}
                  onChange={(e) => setDocumentText(e.target.value)}
                  placeholder="Cole o texto do seu documento aqui..."
                  className="form-control-custom"
                />
              </Form.Group>
              <Button variant="primary" onClick={handleDocumentUpload} disabled={isUploading || !documentText.trim()} className="btn-custom">
                {isUploading ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : 'Carregar Documento'}
              </Button>
              {message && <p className="mt-2 text-success">{message}</p>}
            </Card.Body>
          </Card>

          <Card>
            <Card.Body>
              <Card.Title>Documentos Carregados</Card.Title>
              {uploadedDocuments.length === 0 ? (
                <p>Nenhum documento carregado ainda.</p>
              ) : (
                <ListGroup variant="flush">
                  {uploadedDocuments.map((doc, index) => (
                    <ListGroup.Item key={index} className="text-muted small list-group-item">
                      {doc.substring(0, 100)}...
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Interface de Chat</Card.Title>
              <div ref={chatHistoryRef} className="chat-history" style={{ maxHeight: '400px', overflowY: 'auto', marginBottom: '10px' }}>
                {conversation.length === 0 ? (
                  <p className="text-muted">Comece a conversar! Carregue um documento e faça uma pergunta.</p>
                ) : (
                  conversation.map((msg, index) => (
                    <div key={index} className={`chat-message-container ${msg.type === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
                      <div className={msg.type === 'user' ? 'chat-message-user' : 'chat-message-rag'}>
                        {msg.content}
                      </div>
                    </div>
                  ))
                )}
                {isQuerying && (
                  <div className="d-flex justify-content-start mb-2">
                    <div className="chat-message-rag">
                      <Spinner as="span" animation="dots" size="sm" role="status" aria-hidden="true" /> Pensando...
                    </div>
                  </div>
                )}
              </div>
              <Form.Group className="mb-3">
                <Form.Control
                  as="textarea"
                  rows={2}
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Digite sua pergunta aqui..."
                  className="form-control textarea-chat"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleQueryRag();
                    }
                  }}
                />
              </Form.Group>
              <Button variant="success" onClick={handleQueryRag} disabled={isQuerying || !queryText.trim()} className="btn-custom">
                {isQuerying ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : 'Enviar Pergunta'}
              </Button>
            </Card.Body>
          </Card>

          {retrievedChunks.length > 0 && (
            <Card>
              <Card.Body>
                <Card.Title>Preview de Contexto (Trechos Recuperados)</Card.Title>
                <ListGroup variant="flush">
                  {retrievedChunks.map((chunk, index) => (
                    <ListGroup.Item key={index} className="text-muted small list-group-item">
                      {chunk.substring(0, 200)}...
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;