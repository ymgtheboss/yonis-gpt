# Yonis GPT

Yonis GPT is a desktop chat app built with Python and Flet. It connects to an AI service running through an API on a NAS, so you can send messages and receive answers.

## Core features

- Send a message and see the AI's answer appear as it is generated.
- Start a new conversation whenever you want.
- Display messages with Markdown formatting.
- Show connection and request errors in the app.

## Dependencies

You need **Python 3** and these Python packages:

- **Flet** for the desktop interface.
- **HTTPX** for communication with the API.

Install them in a terminal:

```bash
python3 -m pip install flet httpx
```

The app also needs the NAS API to be running and reachable from your computer. The API server is separate from this app. The default address uses a Tailscale hostname, so you may need to connect to the appropriate Tailscale network. The app does not display previous conversations, but the API may still save them on the NAS.

## How to run

Open a terminal in the project folder and run:

```bash
python3 yonis_chatbot.py
```

A desktop window will open. Type a message and press **Send**. Press **New chat** to start a new conversation.

The API address is set in the code. If you need to use a different API, set the `NOOK_API_URL` environment variable before starting the app.
