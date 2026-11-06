import flet as ft


def main(page: ft.Page):
    page.title = "counter"
    text =ft.Text("0" , size= 110 , left= 350 , top = 50)




    def increase():
        
        text.value=str(int(text.value)+1)
        reset()
        if(page.bgcolor == "blue"):
            page.bgcolor = "green"
        elif (page.bgcolor == "green"):
            page.bgcolor = "red"

        else:
            page.bgcolor = "blue"




        page.update()


    def reset():
        if(text.value=="11"):
            text.value="0"
    

     

    button = ft.Button(
        content=ft.Text("increase" , size = 40),
        on_click=increase,
        top = 350,
        left = 240,
        width = 300,
        height=80





    )
   
        
        

    page.add(ft.Stack(

        width=1000,
        height=1000,
        controls=[button , text]
    ))    
        

   

if __name__ == "__main__":
    ft.run(main)
