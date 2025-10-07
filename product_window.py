#
# окно с таблицей продукции
#
#-------------------------------

from tkinter import *

def ProductWindow(switch_window):
    """Создает главное окно"""
    # Закрываем окно авторизации
    switch_window.withdraw()
    
    # Создаем главное окно
    main_win = Toplevel()
    main_win.title("Главное меню")
    main_win.geometry("800x600")
    
    # Контент главного окна
    Label(main_win, text="Продукты!", font=("Arial", 20)).pack(pady=50)
    
    # Кнопка выхода
    Button(main_win, text="Выйти", 
           command=lambda: exit_app(main_win, switch_window)).pack()

def exit_app(main_window, switch_window):
    """Выход из приложения"""
    main_window.destroy()
    switch_window.destroy()