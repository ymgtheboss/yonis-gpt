import asyncio
import json
import os

import flet as ft
import httpx

API = "https://truenas-scale.tailb323cd.ts.net:10000/nook-api"


async def request(path, data):
    async with httpx.AsyncClient(timeout=20, trust_env=False) as client:
        response = await client.post(API + path, json=data)
        await check(response)
        return response.json()



async def check(response):
    if response.is_error:
        await response.aread()
        response.raise_for_status()


async def main(page: ft.Page):
    page.title = "yonis gpt"
    page.bgcolor = "#F7F5F0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width, page.window.height = 900, 700
    page.window.min_width, page.window.min_height = 600, 500

    current_chat = None
    busy = False
    title = ft.Text("New conversation", size=18, weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER, expand=True)
    status = ft.Text("Ready", size=12, color="#89847A")
    messages = ft.ListView(expand=True, spacing=15, auto_scroll=True)
    prompt = ft.TextField(hint_text="Type a message…", expand=True, multiline=True,
                          min_lines=1, max_lines=5, shift_enter=True)
    easter_image = ft.Image(src="easter.png", width=300, visible=False)



    def show_message(role, message_text):
        text = ft.Text(message_text, selectable=True)
        if role == "user":
            name = "You"
            color = "#ECE8DF"
        else:
            name = "yonis gpt"
            color = "white"
        messages.controls.append(ft.Container(
            bgcolor=color, padding=15, border_radius=12,
            content=ft.Column([ft.Text(name), text]),
        ))
        return text

    def new_chat(e):
        nonlocal current_chat
        if busy:
            return
        current_chat = None
        title.value = "New conversation"
        messages.controls.clear()
        status.value = "Ready"
        page.update()

    async def send(e):
        nonlocal current_chat, busy
        message_text = (prompt.value or "").strip()
        if busy or not message_text:
            return
        



        if message_text.lower() == "lebron":
            busy = True
            send_button.disabled = True
            prompt.value = ""
            easter_image.visible = True
            page.update()
            await asyncio.sleep(2)
            easter_image.visible = False
            send_button.disabled = False
            busy = False
            page.update()
            return

        busy = True
        prompt.value = ""
        send_button.disabled = True
        status.value = "Thinking…"



        page.update()
        try:
            if not current_chat:
                chat = await request("/chats", {"title": message_text[:70]})
                current_chat = chat["id"]
                title.value = chat.get("title", "New conversation")

            show_message("user", message_text)
            answer = show_message("assistant", "Thinking…")
            page.update()
            full_answer = ""


            finished = False
            async with httpx.AsyncClient(timeout=httpx.Timeout(300, connect=15), trust_env=False) as client:
                async with client.stream("POST", f"{API}/chats/{current_chat}/messages",
                                         json={"content": message_text}) as response:
                    await check(response)
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        item = json.loads(line)
                        if item.get("error"):
                            raise RuntimeError(item["error"])
                        full_answer += item.get("delta", "")
                        if item.get("delta"):
                            answer.value = full_answer
                            page.update()
                        if item.get("done"):
                            if not item.get("saved"):

                                raise RuntimeError("Qwen returned no answer. Try again.")
                            


                            finished = True


            if not finished:
                raise RuntimeError("Connection interrupted. Please try again.")
            answer.value = full_answer
            status.value = "Connected"
        except Exception as error:
            status.value = f"Error: {error}"
            prompt.value = message_text


        finally:



            busy = False
            send_button.disabled = False
            page.update()

    prompt.on_submit = send
    send_button = ft.Button("Send", on_click=send)
    page.padding = 20
    page.add(ft.Column([
        ft.Row([ft.Button("New chat", on_click=new_chat), title]),
        ft.Divider(), ft.Row([easter_image], alignment=ft.MainAxisAlignment.CENTER),
        messages, status, ft.Row([prompt, send_button]),
    ], expand=True))


if __name__ == "__main__":
    ft.run(main, assets_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"))
