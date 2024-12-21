Build a messaging App with django rest framework
    AUTH
        http://127.0.0.1:8000/api-auth/login
        Endpoint: POST /api/signup/

    Conversations
        GET /api/conversations/
        POST /api/conversations/
        GET /api/conversations/<id>/
    Messages
        GET /api/conversations/<conversation_id>/messages/
        POST /api/conversations/<conversation_id>/messages/

