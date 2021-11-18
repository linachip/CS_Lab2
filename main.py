from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
import json

main = Tk()
main.title('Laboratory work #2')
main.geometry('1000x600')
main.configure(bg='#5d5fef')
font = Font(family="Raleway", size=12)

global selected
selected = False

start_match = []
end_match = []
word_index = 0
custom_items_used = []
jsons_no = 0
to_json = {}
extension = ''
current_file = ''


#function to create new file
def newFile():
    my_text.delete('1.0', END)

    main.title('New File')
    status_bar.config(text='New File       ')


def findAll(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


#function to open file
def openFile():
    global jsons_no
    global to_json
    global extension
    global current_file

    my_text.delete('1.0', END)

    text_file = filedialog.askopenfilename(
        initialdir='lab2/audit/',
        title='Open File', filetypes=(('All Files', '*.*'),))

    current_file = text_file


    name = text_file
    status_bar.config(text=f'{name}       ')
    name = name.replace('lab2/', '')
    main.title(f'{name}')

    extension = ''
    i = len(name) - 1
    while name[i] != '.':
        extension += name[i]
        i -= 1
    extension = extension[::-1]


    if extension == 'audit':
        text_file = open(text_file, 'r')
        contents = text_file.read()

        contents = contents.replace('            :', ':')
        contents = contents.replace('           :', ':')
        contents = contents.replace('          :', ':')
        contents = contents.replace('         :', ':')
        contents = contents.replace('        :', ':')
        contents = contents.replace('       :', ':')
        contents = contents.replace('      :', ':')
        contents = contents.replace('     :', ':')
        contents = contents.replace('    :', ':')
        contents = contents.replace('   :', ':')
        contents = contents.replace('  :', ':')
        contents = contents.replace(' :', ':')

        start = list(findAll(contents, '<custom_item>'))
        ending = list(findAll(contents, '</custom_item>'))

        custom_item = {}

        custom_item['REGISTRY_SETTING'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [],
                                       'reg_item': [], 'reg_option': [], 'info': []}
        custom_item['AUDIT_POWERSHELL'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                       'powershell_args': [],
                                       'only_show_cmd_output': [], 'check_type': [], 'severity': [], 'appcmd_list': [],
                                       'appcmd_filter': [], 'appcmd_filter_value': []}
        custom_item['PASSWORD_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                      'check_type': [],
                                      'password_policy': []}
        custom_item['LOCKOUT_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                     'check_type': [],
                                     'lockout_policy': []}
        custom_item['USER_RIGHTS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                         'check_type': [],
                                         'right_type': []}
        custom_item['CHECK_ACCOUNT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [],
                                    'account_type': []}
        custom_item['BANNER_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [],
                                   'reg_item': [], 'is_substring': []}
        custom_item['AUDIT_POLICY_SUBCATEGORY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                               'check_type': [],
                                               'audit_policy_policy': []}
        custom_item['REG_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                'reg_key': [], 'reg_item': [], 'key_item': []}
        custom_item['ANONYMOUS_SID_SETTING'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                            'check_type': []}

        general_custom_item = {}
        general_custom_item_keys = []

        for key in custom_item:
            keys_list = list(custom_item[key])
            for key_x in keys_list:
                if key_x not in general_custom_item_keys:
                    general_custom_item_keys.append(key_x)

        general_custom_item['custom_item_number'] = []

        for key in general_custom_item_keys:
            general_custom_item[key] = []

        general_custom_item['type'] = []
        general_custom_item['description'] = []
        general_custom_item['info'] = []
        general_custom_item['see_also'] = []

        for i in range(len(start)):
            content_type_block = contents[start[i] + 13: ending[i]]
            general_custom_item['custom_item_number'].append(i)
            for element in list(general_custom_item.keys()):
                element_length = len(element) + 1
                if content_type_block.find(element) != -1:
                    general_custom_item[element].append(content_type_block[content_type_block.find(
                        element + ':') + element_length: content_type_block[content_type_block.find(
                        element + ':') + element_length:].find('\n') + content_type_block.find(
                        element + ':') + element_length].strip())
                else:
                    if element != 'custom_item_number':
                        general_custom_item[element].append('')

        jsons_no = len(general_custom_item['custom_item_number'])

        to_json = []
        for i in range(len(general_custom_item['type'])):
            to_print = {}
            for element in list(general_custom_item.keys()):
                if general_custom_item[element][i] != '':
                    to_print[element] = general_custom_item[element][i]
            to_json.append(to_print)

        my_text.insert(END, json.dumps(to_json, indent=4))


        text_file.close()

    elif extension == 'json':
        text_file = open(text_file, 'r')
        to_json = json.load(text_file)
        jsons_no = len(to_json)
        my_text.insert(END, json.dumps(to_json, indent=4))
        text_file.close()


def saveFile():
    text_file = filedialog.asksaveasfilename(
        defaultextension='.*',
        initialdir='lab2/audit/',
        title='Save File', filetypes=(('All Files', '*.*'),)
        )

    if text_file:
        name = text_file
        status_bar.config(text=f'{name}       ')
        name = name.replace('lab2/audit/', '')
        main.title(f'{name}')

        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        text_file.close()


#function to save as file
def saveAs():
    global jsons_no
    global to_json
    global extension

    def check():
        global custom_items_used
        global jsons_no
        global to_json
        global extension
        global current_file

        custom_items_used = []

        for i in range(len(check_btns)):
            if var[i].get() == 1:
                custom_items_used.append(i)

        main_checkbox.destroy()


        text_file = filedialog.asksaveasfilename(
                defaultextension='.*',
                initialdir='lab2/audit/',
                title='Save File', filetypes=(('All Files', '*.*'),))

        if text_file:
            name = text_file
            status_bar.config(text=f'{name}       ')
            name = name.replace('lab2/audit/', '')
            main.title(f'{name}')

            to_print = []
            for i in custom_items_used:
                to_print.append((to_json[i]))

            text_file = open(text_file, 'w')
            json.dump(to_print, text_file, indent=4)

            text_file.close()

    def selectAll():
        for i in range(len(check_btns)):
            var[i].set(1)

    def selectNone():
        for i in range(len(check_btns)):
            var[i].set(0)

    main_checkbox = Tk()
    main_checkbox.title('Select the custom items')

    checkbox_scroll = Scrollbar(main_checkbox, orient='vertical')
    checkbox_scroll.pack(side=RIGHT, fill=Y)

    checkbox_txt = Text(main_checkbox, width=50, height=30, yscrollcommand=checkbox_scroll.set)

    checkbox_scroll.config(command=checkbox_txt.yview)

    var = []
    for i in range(jsons_no):
        var.append(IntVar(main_checkbox))
    checkbox_txt.pack(side=TOP, fill=BOTH, expand=True)
    check_btns = [Checkbutton(main_checkbox, text="custom item № %s" % i, variable=var[i], onvalue=1, offvalue=0, )
                    for i in range(jsons_no)]
    for chk_btn in check_btns:
        checkbox_txt.window_create('end', window=chk_btn)
        checkbox_txt.insert('end', '\n')

    submit_btn = Button(main_checkbox, text='Submit', bg="red", fg="white", width=10, height=1)
    submit_btn.pack(side=BOTTOM)
    submit_btn.config(command=check)

    select_all_btn = Button(main_checkbox, text='Select All', bg="#222222", fg="white", width=10, height=1)
    select_all_btn.pack(side=TOP)
    select_all_btn.config(command=selectAll)

    select_none_btn = Button(main_checkbox, text='Deselect All', bg="#ffffff", fg="black", width=10, height=1)
    select_none_btn.pack(side=TOP)
    select_all_btn.config(command=selectNone)

    main_checkbox.mainloop()

def exportFile():
    global jsons_no
    global to_json
    global extension

    def check():
        global custom_items_used
        global jsons_no
        global to_json
        global extension
        global current_file

        custom_items_used = []

        for i in range(len(check_btns)):
            if var[i].get() == 1:
                custom_items_used.append(i)

        main_checkbox.destroy()

        text_file = filedialog.asksaveasfilename(
            defaultextension='.*',
            initialdir='lab2/audit/',
            title='Save File', filetypes=(('All Files', '*.*'),))

        if text_file:
            name = text_file
            status_bar.config(text=f'{name}       ')
            name = name.replace('lab2/audit/', '')
            main.title(f'{name}')

        text_file = open(text_file, 'w')

        to_print = []
        for i in custom_items_used:
            text_file.write('<custom_item>\n')
            for j in to_json[i]:
                text_file.write('\t' + j + ' : ' + str(to_json[i][j]) + '\n')
                text_file.write('</custom_item>\n')

            text_file.close()

    def selectAll():
        for i in range(len(check_btns)):
            var[i].set(1)

    def selectNone():
        for i in range(len(check_btns)):
            var[i].set(0)

    main_checkbox = Tk()
    main_checkbox.title('Select the custom items')

    checkbox_scroll = Scrollbar(main_checkbox, orient='vertical')
    checkbox_scroll.pack(side=RIGHT, fill=Y)

    checkbox_txt = Text(main_checkbox, width=80, height=50, yscrollcommand=checkbox_scroll.set)

    checkbox_scroll.config(command=checkbox_txt.yview)

    var = []
    for i in range(jsons_no):
        var.append(IntVar(main_checkbox))
    checkbox_txt.pack(side=TOP, fill=BOTH, expand=True)
    check_btns = [Checkbutton(main_checkbox, text="custom item № %s" % i, variable=var[i], onvalue=1, offvalue=0, )
                  for i in range(jsons_no)]
    for chk_btn in check_btns:
        checkbox_txt.window_create('end', window=chk_btn)
        checkbox_txt.insert('end', '\n')

    submit_btn = Button(main_checkbox, text='Submit', bg="red", fg="white", width=10, height=1)
    submit_btn.pack(side=BOTTOM)
    submit_btn.config(command=check)

    select_all_btn = Button(main_checkbox, text='Select All', bg="#222222", fg="white", width=10, height=1)
    select_all_btn.pack(side=TOP)
    select_all_btn.config(command=selectAll)

    select_none_btn = Button(main_checkbox, text='Deselect All', bg="#ffffff", fg="black", width=10, height=1)
    select_none_btn.pack(side=TOP)
    select_all_btn.config(command=selectNone)

    main_checkbox.mainloop()

def find():
    global start_match
    global end_match
    global word_index

    start_match = []
    end_match = []
    word_index = 0

    my_text.tag_remove('found', '1.0', END)

    searched_word = search_bar.get()

    if searched_word:
        index = '1.0'
        while 1:
            index = my_text.search(searched_word, index, nocase=1, stopindex=END)
            if not index: break

            start_match.append(index)

            last_index = '%s+%dc' % (index, len(searched_word))
            end_match.append(last_index)

            index = last_index

        next_word()

def next_word():
    global word_index
    global start_match
    global end_match

    if word_index < len(start_match):
        my_text.tag_remove('found', '1.0', END)
        index = start_match[word_index]
        last_index = end_match[word_index]
        my_text.tag_add('found', index, last_index)
        to_see = int(index[0:index.find('.')])
        my_text.yview(to_see - 10)
        if word_index < (len(start_match) - 1):
            word_index += 1
        my_text.tag_config('found', foreground='black', background='yellow')

def previous_word():
    global word_index
    global start_match
    global end_match

    if word_index >= 0:
        my_text.tag_remove('found', '1.0', END)
        index = start_match[word_index]
        last_index = end_match[word_index]
        my_text.tag_add('found', index, last_index)
        to_see = int(index[0:index.find('.')])
        my_text.yview(to_see - 10)
        if word_index > 0:
            word_index -= 1
        my_text.tag_config('found', foreground='black', background='yellow')


label = ttk.Label(text='Search Bar')
label.pack(ipady=5, ipadx=10)
label.place(relx=0.25, rely=0.02)
search_bar = Entry(main, font=("Raleway", 12))
search_bar.pack(ipady=5, ipadx=100)

search_bar.focus_set()

search_btn = Button(search_bar, text='Find')
search_btn.pack(side=RIGHT)
search_btn.config(command=find)

next_button = Button(search_bar, text='Next')
next_button.pack(side=RIGHT)
next_button.config(command=next_word)

back_button = Button(search_bar, text='Previous')
back_button.pack(side=RIGHT)
back_button.config(command=previous_word)

#main frame
my_frame = Frame(main)
my_frame.pack(pady=5)

#scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

horizontal_scroll = Scrollbar(my_frame, orient='horizontal')
horizontal_scroll.pack(side=BOTTOM, fill=X)

#text
my_text = Text(my_frame, width=80, height=25, font=font,
               undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=horizontal_scroll.set)
my_text.pack()

text_scroll.config(command=my_text.yview)
horizontal_scroll.config(command=my_text.xview)

#menu
my_menu = Menu(main)
main.config(menu=my_menu)

file_menu = Menu (my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=newFile)
file_menu.add_command(label='Open', command=openFile)
file_menu.add_command(label='Save', command=saveFile)
file_menu.add_command(label='Save As', command=saveAs)
file_menu.add_command(label='Export', command=exportFile)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=main.quit)


status_bar = Label(main, text='Start     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=10)

main.mainloop()
