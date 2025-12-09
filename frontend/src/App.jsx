import { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [topic, setTopic] = useState('')
  const [sendEmail, setSendEmail] = useState(false)
  const [emailAddress, setEmailAddress] = useState('')
  const [createTrello, setCreateTrello] = useState(false)
  const [trelloListId, setTrelloListId] = useState('')
  const [loading, setLoading] = useState(false)
  const [tasks, setTasks] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    fetchTasks()
    // Actualizar cada 5 segundos
    const interval = setInterval(fetchTasks, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/research/tasks/`)
      setTasks(response.data)
    } catch (err) {
      console.error('Error fetching tasks:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const payload = {
        topic,
        send_email: sendEmail,
        email_address: sendEmail ? emailAddress : null,
        create_trello_card: createTrello,
        trello_list_id: createTrello ? trelloListId : null,
      }

      await axios.post(`${API_URL}/research/tasks/`, payload)

      // Limpiar formulario
      setTopic('')
      setSendEmail(false)
      setEmailAddress('')
      setCreateTrello(false)
      setTrelloListId('')

      // Actualizar lista de tareas
      setTimeout(fetchTasks, 1000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear la tarea de investigación')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('es-ES')
  }

  const getStatusClass = (status) => {
    return `task-status status-${status}`
  }

  const getStatusText = (status) => {
    const statusMap = {
      pending: 'Pendiente',
      processing: 'Procesando',
      completed: 'Completado',
      failed: 'Fallido'
    }
    return statusMap[status] || status
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>IntelliAgent</h1>
          <p>Ecosistema Inteligente para la Automatización de la Investigación</p>
        </header>

        <main className="main-content">
          <section className="research-form">
            <h2>Nueva Investigación</h2>
            {error && <div className="error-message">{error}</div>}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="topic">Tema de Investigación</label>
                <input
                  type="text"
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Ej: Inteligencia Artificial en la medicina"
                  required
                />
              </div>

              <div className="form-group">
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="sendEmail"
                    checked={sendEmail}
                    onChange={(e) => setSendEmail(e.target.checked)}
                  />
                  <label htmlFor="sendEmail">Enviar resultados por correo</label>
                </div>

                {sendEmail && (
                  <input
                    type="email"
                    value={emailAddress}
                    onChange={(e) => setEmailAddress(e.target.value)}
                    placeholder="correo@ejemplo.com"
                    style={{ marginTop: '10px' }}
                    required
                  />
                )}
              </div>

              <div className="form-group">
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="createTrello"
                    checked={createTrello}
                    onChange={(e) => setCreateTrello(e.target.checked)}
                  />
                  <label htmlFor="createTrello">Crear tarjeta en Trello</label>
                </div>

                {createTrello && (
                  <input
                    type="text"
                    value={trelloListId}
                    onChange={(e) => setTrelloListId(e.target.value)}
                    placeholder="ID de lista de Trello"
                    style={{ marginTop: '10px' }}
                    required
                  />
                )}
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Procesando...' : 'Iniciar Investigación'}
              </button>
            </form>
          </section>

          <section className="tasks-list">
            <h2>Investigaciones Recientes</h2>

            {tasks.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📚</div>
                <p>No hay investigaciones aún. Crea una nueva para comenzar.</p>
              </div>
            ) : (
              tasks.map((task) => (
                <div key={task.id} className="task-card">
                  <div className="task-header">
                    <div>
                      <h3 className="task-title">{task.topic}</h3>
                      <div className="task-meta">
                        Creado: {formatDate(task.created_at)}
                      </div>
                    </div>
                    <span className={getStatusClass(task.status)}>
                      {getStatusText(task.status)}
                    </span>
                  </div>

                  {task.result && (
                    <div className="task-result">
                      <h4>Resumen</h4>
                      <p>{task.result.summary}</p>

                      {task.result.key_data && Object.keys(task.result.key_data).length > 0 && (
                        <div className="key-data">
                          <h4>Datos Clave</h4>
                          <pre>{JSON.stringify(task.result.key_data, null, 2)}</pre>
                        </div>
                      )}

                      {task.result.sources && task.result.sources.length > 0 && (
                        <div style={{ marginTop: '10px' }}>
                          <strong>Fuentes:</strong> {task.result.sources.join(', ')}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
