import os
import tkinter as tk
import customtkinter as ctk
import schedule
import time
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from gmail_methods import gmail_send_message, search_emails, delete_emails

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        app_width = 1200
        app_height = 600
        
        self.title("Gmail Organizer")

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(os.getcwd() + "/theme.json")

        self.center_window(app_width, app_height)
        ttk.Style(self).theme_use('clam')

        ### grid layout setting ###
        self.grid_columnconfigure((0, 3), weight=0)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        ### global variables ###
        self.selected_time = None
        self.sent_email = None

        ### left sidebar ###
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")

        self.left_logo_label = ctk.CTkLabel(self.sidebar_frame, text="Gmail Orgainzer", font=ctk.CTkFont(size=20, weight="bold"))
        self.left_logo_label.grid(row=0, column=0, padx=20, pady=(20, 40))

        self.send_btn = ctk.CTkButton(self.sidebar_frame, text="Send", command=lambda: self.selected_page("send"), width=200, height=40, anchor="w", fg_color="transparent")
        self.send_btn.grid(row=1, column=0, padx=(20, 20))

        self.schedule_send_btn = ctk.CTkButton(self.sidebar_frame, text="Schedule Send", command=lambda: self.selected_page("schedule_send"), width=200, height=40, anchor="w", fg_color="transparent")
        self.schedule_send_btn.grid(row=2, column=0, padx=(20, 20))
        self.delete_btn = ctk.CTkButton(self.sidebar_frame, text="Delete", command=lambda: self.selected_page("delete"), width=200, height=40, anchor="w", fg_color="transparent")
        self.delete_btn.grid(row=3, column=0, padx=(20,20))

        ### right sidebar ###
        self.sidebar_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=5, sticky="nsew")

        self.right_logo_label = ctk.CTkLabel(self.sidebar_frame, text="Settings", font=ctk.CTkFont(size=15))
        self.right_logo_label.grid(row=0, column=3, padx=20, pady=(20, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:")
        self.appearance_mode_label.grid(row=1, column=3, padx=20, pady=(10, 0))
        self.theme_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.theme_option.grid(row=2, column=3, padx=20, pady=(10, 10))


        ### default values ###
        self.theme_option.set("System")
        #self.scale_option.set("100%")

        self.schedule_send_page = ctk.CTkFrame(self, corner_radius=0)
        self.schedule_send_page.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        self.delete_page = ctk.CTkFrame(self, corner_radius=0)
        self.delete_page.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        self.send_btn.configure(fg_color=("#d3d3d3", "#007aff"))        
        self.open_sendPage(True)


    ### help functions ###
    def center_window(self, width: int, height: int) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def selected_page(self, page_selected: str) -> None:
        if page_selected == "send":
            self.send_btn.configure(fg_color=("#d3d3d3", "#007aff"))
            self.schedule_send_btn.configure(fg_color="transparent")
            self.delete_btn.configure(fg_color="transparent")

            self.open_sendPage(True)
            self.open_schedule_sendPage(False)
            self.open_deletePage(False)
        elif page_selected == "schedule_send":
            self.send_btn.configure(fg_color="transparent")
            self.schedule_send_btn.configure(fg_color=("#d3d3d3", "#007aff"))
            self.delete_btn.configure(fg_color="transparent")

            self.open_sendPage(False)
            self.open_schedule_sendPage(True)
            self.open_deletePage(False)
        else:
            self.send_btn.configure(fg_color="transparent")
            self.schedule_send_btn.configure(fg_color="transparent")
            self.delete_btn.configure(fg_color=("#d3d3d3", "#007aff"))

            self.open_sendPage(False)
            self.open_schedule_sendPage(False)
            self.open_deletePage(True)

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        ctk.set_appearance_mode(new_appearance_mode)

    def open_sendPage(self, showPage: bool) -> None:
        if showPage:
            self.send_page = ctk.CTkFrame(self, corner_radius=0)
            self.send_page.grid(row=0, column=1, rowspan=5, columnspan=2, padx=10, sticky="nsew")

            self.send_page_from_lbl = ctk.CTkLabel(self.send_page, text="From", width=50, anchor="w").grid(row=0, column=1)
            self.input_from = ctk.CTkEntry(self.send_page, placeholder_text="Your name", width=620)
            self.input_from.grid(row=0, column=2, padx=(30,0), pady=10)

            self.send_page_to_lbl = ctk.CTkLabel(self.send_page, text="To", width=50, anchor='w').grid(row=1, column=1)
            self.input_to = ctk.CTkEntry(self.send_page, placeholder_text="Recipient email", width=620)
            self.input_to.grid(row=1, column=2, padx=(30, 0), pady=(10, 20))

            self.send_page_msg_lbl = ctk.CTkLabel(self.send_page, text="Message", width=50, anchor="w").grid(row=2, column=1, padx=(10,0), pady=(0,10))
            self.send_page_msg_txt = ctk.CTkTextbox(self.send_page, width=710, height=200)
            self.send_page_msg_txt.grid(row=3, column=1, columnspan=2, sticky='w', padx=(15,0))

            self.send_page_btn = ctk.CTkButton(self.send_page, text="Send", width=80, command=self.getInputValues)
            self.send_page_btn.grid(row=4, column=1, sticky='W', padx=(15,0), pady=(20,0))
        else:
            self.send_page.grid_forget()

    def open_schedule_sendPage(self, showPage: bool) -> None:
        if showPage:
            self.schedule_send_page = ctk.CTkFrame(self, corner_radius=0)
            self.schedule_send_page.grid(row=0, column=1, rowspan=5, columnspan=2, padx=15, sticky="nsew")

            self.send_page_from_lbl = ctk.CTkLabel(self.schedule_send_page, text="From", width=50, anchor="w").grid(row=0, column=1, sticky='w', padx=(15,0))
            self.input_from_schedule = ctk.CTkEntry(self.schedule_send_page, placeholder_text="Your name", width=600)
            self.input_from_schedule.grid(row=0, column=2, pady=10)

            self.send_page_to_lbl = ctk.CTkLabel(self.schedule_send_page, text="To", width=50, anchor='w').grid(row=1, column=1, sticky='w', padx=(15,0))
            self.input_to_schedule = ctk.CTkEntry(self.schedule_send_page, placeholder_text="Recipient email", width=600)
            self.input_to_schedule.grid(row=1, column=2, pady=(15, 20))

            self.msg_lbl_schedule = ctk.CTkLabel(self.schedule_send_page, text="Message", width=50, anchor="w").grid(row=2, column=1, padx=(15,0), pady=(0,10), sticky='w')
            self.msg_txt_schedule = ctk.CTkTextbox(self.schedule_send_page, width=710, height=200)
            self.msg_txt_schedule.grid(row=3, column=1, columnspan=2, sticky='w', padx=(15,0))

            self.set_schedule_lbl = ctk.CTkLabel(self.schedule_send_page, text="Your email will be send:", width=80, anchor='w').grid(row=4, column=1, sticky='w', padx=(15,0), pady=(30,10), columnspan=2)

            self.schedule_option = ctk.CTkOptionMenu(self.schedule_send_page, values=["Select an option", "After 5 minutes", "After 10 minutes", "After 30 minutes", "After 1 hour", "Aftet 2 hours", "After 3 hours"], width=150, command=self.selectTime)
            self.schedule_option.grid(row=4, column=1, padx=(200,0), pady=(30,10), columnspan=2, sticky='w')

            

            # self.calendar_schedule = self.createCalendar(self.schedule_send_page, "schedule")
            # self.calendar_schedule.grid(row=2, column=2)
            # self.select_btn = ctk.CTkButton(self.schedule_send_page, text="Select", width=206, command=self.getSelected_Schedule_Date)
            # self.select_btn.grid(row=3, column=2)
            
            # self.selected_date = ctk.CTkLabel(self.schedule_send_page, text="Scheduled date: ", anchor='w', width=100)
            # self.selected_date.grid(row=2, column=1, sticky='w', padx=(30,0))
            # self.selected_date_input = ctk.CTkEntry(self.schedule_send_page, placeholder_text="mm/dd/yyyy")
            # self.selected_date_input.grid(row=2, column=2, sticky='w')

            self.schedule_btn = ctk.CTkButton(self.schedule_send_page, text="Schedule", width=80, command=self.scheduleEmail)
            self.schedule_btn.grid(row=6, column=1, sticky='w', padx=(15,0), pady=(20,0))
            
        else:
            self.schedule_send_page.grid_forget()

    def open_deletePage(self, showPage: bool) -> None:
        if showPage:
            self.delete_page = ctk.CTkFrame(self, corner_radius=0)
            self.delete_page.grid(row=0, column=1, rowspan=5, columnspan=2, padx=10, sticky="nsew")
            
            self.delete_page_lbl = ctk.CTkLabel(self.delete_page, text="Select date range", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=1, columnspan=2, sticky='w', padx=(10,0), pady=(10,20))

            self.start_calendar = self.createCalendar(self.delete_page, "delete")
            self.start_calendar.grid(row=1, column=1, sticky='w', padx=30)
            self.start_date_select = ctk.CTkButton(self.delete_page, text="Select", width=206, command=self.getSelected_startDate)
            self.start_date_select.grid(row=2, column=1, pady=(0,10))

            self.end_calendar = self.createCalendar(self.delete_page, "delete")
            self.end_calendar.grid(row=1, column=2, padx=(130,0))
            self.end_date_select = ctk.CTkButton(self.delete_page, text="Select", width=206, command=self.getSelected_endDate)
            self.end_date_select.grid(row=2, column=2, padx=(130, 0), pady=(0,10))

            self.start_date_lbl = ctk.CTkLabel(self.delete_page, text="Start date:").grid(row=3, column=1, sticky='w', padx=(30,10))
            self.start_date_input = ctk.CTkEntry(self.delete_page, placeholder_text="mm/dd/yyyy")
            self.start_date_input.grid(row=3, column=1, padx=(80,0))

            self.end_date_lbl = ctk.CTkLabel(self.delete_page, text="End date:").grid(row=3, column=2, padx=(0,10))
            self.end_date_input = ctk.CTkEntry(self.delete_page, placeholder_text="mm/dd/yyyy")
            self.end_date_input.grid(row=3, column=2, padx=(200,0))

            self.delete_btn = ctk.CTkButton(self.delete_page, text="Delete", width=80, command=self.deleteEmail)
            self.delete_btn.grid(row=6, column=2, sticky='W', pady=(30, 0))

        else:
            self.delete_page.grid_forget()

    def getInputValues(self) -> None:
        gmail_send_message(self.input_to.get(), self.input_from.get(), self.send_page_msg_txt.get("1.0", "end-1c"))

    def selectTime(self, selected: str) -> None:
        self.selected_time = selected

    def scheduleEmail(self) -> None:
        option_selected = self.selected_time.split(' ')
        schedule_time = self.calculateScheduleTime(option_selected[2], int(option_selected[1]))
        #schedule.every(3).seconds.do(self.setSchedule)
        schedule.every().day.at(schedule_time).do(self.setSchedule)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def setSchedule(self) -> schedule.CancelJob:
        self.sent_email = gmail_send_message(self.input_to_schedule.get(),self.input_from_schedule.get(), self.msg_txt_schedule.get("1.0", "end-1c"))

        return schedule.CancelJob

    def calculateScheduleTime(self, time_selected: str, time_length: int) -> str:
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute

        if (time_selected == "minutes"):
            schedule_hour = current_hour
            schedule_minute = current_minute + time_length

            if (schedule_minute > 59):
                schedule_minute = schedule_minute - 60
                schedule_hour = current_hour + 1
        else:
            schedule_hour  = current_hour + time_length
            schedule_minute = current_minute

            if (schedule_hour > 23):
                schedule_hour = schedule_hour - 24

        return str(schedule_hour) + ":" + str(schedule_minute)

    def deleteEmail(self) -> str:
        endDate_info = self.end_date_input.get().split('/')
        endDate_info[1] = str(int(endDate_info[1]) + 1)
        format_endDate = '/'.join(endDate_info)
        query = "after:" + self.start_date_input.get() + " before:" + format_endDate
        print(query)
        results = search_emails(query)
        delete_emails(results, self.start_date_input.get(), format_endDate)

    def createCalendar(self, pageName: ctk.CTkFrame, type: str) -> Calendar:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day

        calendar = Calendar(pageName,
                            mindate= datetime(year, month, day) if type == "schedule" else datetime(year-1, month, day),
                            maxdate=datetime(year+1, month, day) if type == "schedule" else datetime(year, month, day),
                            date_pattern="mm/dd/yyyy",
                            showweeknumbers= False,
                            showothermonthdays=False,
                            background="#d3d3d3", 
                            disabledbackground="#d3d3d3", 
                            bordercolor="#d3d3d3",
                            headersbackground="#d3d3d3", 
                            normalbackground="#d3d3d3", 
                            foreground='black',
                            normalforeground='black', 
                            headersforeground='black', 
                            weekendforeground="red",
                            selectbackground= "#007aff")
        return calendar

    def getSelected_Schedule_Date(self) -> None:
        self.selected_date_input.delete(0, tk.END)
        self.selected_date_input.insert(0, self.calendar_schedule.get_date())

    def getSelected_startDate(self) -> None:
        self.start_date_input.delete(0, tk.END)
        self.start_date_input.insert(0, self.start_calendar.get_date())

    def getSelected_endDate(self) -> None:
        self.end_date_input.delete(0, tk.END)
        self.end_date_input.insert(0, self.end_calendar.get_date())

# start App
app = App()
app.mainloop()