import requests
from bs4 import BeautifulSoup
import tkinter
from tkinter.ttk import *
from PIL import Image, ImageTk


def codeSyntaxReturner(url):
    dirLinkList = list()
    dirLinkList.append(url)
    req = requests.get(url)
    repoLinkProtocol = url[:8]
    linkDivide = url.split("/")
    domainName = linkDivide[2]
    soup = BeautifulSoup(req.content, "html.parser")
    allHyperlinkTags = soup.find_all('a')
    for hyperLinkTags in allHyperlinkTags:
        strHyperLinkTag = str(hyperLinkTags)
        if f'{linkDivide[3]}/{linkDivide[4]}/tree/master/' in strHyperLinkTag:
            splitFileTags = strHyperLinkTag.split(' ')
            for href in splitFileTags:
                if href[0:4] == "href":
                    link = href[6:-1]
                    dirLinkList.append(repoLinkProtocol + domainName + link)

    codeLinksList = list()
    for url in dirLinkList:
        req = requests.get(url)
        repoName = f'/{linkDivide[3]}/{linkDivide[4]}'
        soup = BeautifulSoup(req.content, "html.parser")
        codeExtensionsList = [".py", ".cpp", ".java", "json", ".c"]

        allHyperlinkTags = soup.find_all('a')
        for hyperlinkTag in allHyperlinkTags:
            for ext in codeExtensionsList:
                strHyperLinkTag = str(hyperlinkTag)
                if ext in strHyperLinkTag and not (".com" in strHyperLinkTag):
                    splitTag = strHyperLinkTag.split(' ')
                    for href in splitTag:
                        if href[0:4] == "href":
                            link1 = href[6:-1]
                            codeLinksList.append(repoLinkProtocol + domainName + link1)
        for link2 in codeLinksList:
            if f'{repoLinkProtocol + domainName + repoName}/blob/master/' in link2:
                pass
            else:
                codeLinksList.remove(link2)
    program = []
    for code_link in codeLinksList:
        req = requests.get(code_link)
        soup = BeautifulSoup(req.content, "html.parser")
        code = soup.text
        code1 = code.split('\n')  # to ignore the '\n' char in the variable code
        code2 = [ele for ele in code1 if ele.strip()]  # to ignore the empty or blank elements in variable code_1
        for i in range(len(code2)):
            found = 0
            if "View blame" in code2[i]:
                found = True
            while found:
                if "Copy lines" in code2[i]:
                    found = False
                if code2[i] == "                View blame" or code2[i] == "            Copy lines":
                    pass
                else:
                    program.append(code2[i])
                i = i + 1
    return program


# Function Which clear the frame
def clearFrame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


# Function to Display all the Code in the Repo
def displayCodesButton(link, frame):
    code = codeSyntaxReturner(link)
    vulnerableSyntaxList, vulnerableDescriptionList, vulnerableRatingList = returnVulnerable(link)

    clearFrame(frame)

    verticalScrollbarTextBox = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
    verticalScrollbarTextBox.grid(column=1, sticky='ns')

    textBox = tkinter.Text(frame, height=20, width=130,  yscrollcommand=verticalScrollbarTextBox.set)
    for i in range(len(code)):
        textBox.insert(float(i + 1), code[i] + '\n')

    verticalScrollbarTextBox.config(command=textBox.yview)

    textBox.grid(column=0, row=0, sticky='nsew', pady=5, padx=5)
    # Rate Repo Button
    rateButton = tkinter.Button(frame, text='Rate Repo', command=lambda: showRateButton(frame, vulnerableRatingList))
    rateButton.grid(row=1, column=0, sticky='s')


# this adds the vulnerabilities into the file
def addVulnerabilityButton(syn, des, rate, frame_1):
    f = open("vulnerable_syntax.txt", "a")
    f.write(f'{syn.get()}, {des.get()}, {rate.get()}\n')
    f.close()
    addVulnerableSyntax(frame_1)


# Shows when Add Vulnerability is Clicked
def addVulnerableSyntax(frame):
    def synTempText(w):
        syntaxEntry.delete(0, "end")

    def descTempText(w):
        descriptionEntry.delete(0, "end")

    def rateTempText(w):
        effectRatingEntry.delete(0, "end")

    clearFrame(frame)

    # Entry Variable declaration
    syntax = tkinter.StringVar()
    desc = tkinter.StringVar()
    rateSyntax = tkinter.StringVar()

    # Main frame for adding widgets
    mainFrame = tkinter.Frame(frame)
    mainFrame.grid(sticky='nsew', padx=5)

    # Main frame column Configuration
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.columnconfigure(1, weight=10)

    # title label and all functionality widgets
    title_label = tkinter.Label(mainFrame, text='Add Vulnerable Syntax', font=('Arial', 20))
    title_label.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5, padx=5)

    # Sub Frame
    subFrame = tkinter.Frame(mainFrame)
    subFrame.grid(row=1, column=1, pady=5, padx=5, sticky='ns')

    # Syntax
    syntaxLabel = tkinter.Label(subFrame, text='Syntax', font=('Arial', 15))
    syntaxLabel.grid(column=0, row=0, sticky='e', padx=5, pady=5)

    # Syntax Entry
    syntaxEntry = tkinter.Entry(subFrame, textvariable=syntax, width=50)
    syntaxEntry.insert(0, "Enter the Vulnerable Syntax")
    syntaxEntry.grid(column=1, row=0, sticky='w', padx=5, pady=5)
    syntaxEntry.bind("<FocusIn>", synTempText)

    # Description
    descriptionLabel = tkinter.Label(subFrame, text='Description', font=('Arial', 15))
    descriptionLabel.grid(column=0, row=1, sticky='e', padx=5, pady=5)

    # Description Entry
    descriptionEntry = tkinter.Entry(subFrame, textvariable=desc, width=50)
    descriptionEntry.insert(0, "Describe the Vulnerability")
    descriptionEntry.grid(column=1, row=1, sticky='w', padx=5, pady=5)
    descriptionEntry.bind("<FocusIn>", descTempText)

    # Rating
    dangerRatingLabel = tkinter.Label(subFrame, text='Syntax Danger Rating', font=('Arial', 15))
    dangerRatingLabel.grid(column=0, row=2, sticky='e', padx=5, pady=5)

    # Danger Rating Entry
    effectRatingEntry = tkinter.Entry(subFrame, textvariable=rateSyntax, width=50)
    effectRatingEntry.insert(0, "Severity of Syntax 1: Low, 2: Medium, 3: High")
    effectRatingEntry.grid(column=1, row=2, sticky='w', padx=5, pady=5)
    effectRatingEntry.bind("<FocusIn>", rateTempText)

    frame.update()

    # Submit Button
    submitButton = tkinter.Button(subFrame, text='Add', command=lambda: addVulnerabilityButton(syntax, desc, rateSyntax, frame))
    submitButton.grid(column=0, row=4, columnspan=2, pady=5)


# Function which returns the Vulnerabilities
def returnVulnerable(link):
    f = open("vulnerable_syntax.txt", "r")
    syntaxList = codeSyntaxReturner(link)
    data = f.read().split('\n')
    data.pop()
    dataList = list()
    vulnerableSyntaxList = list()
    vulnerableDescriptionList = list()
    vulnerableRatingList = list()
    for i in range(len(data)):
        if data[i] == '':
            pass

        else:
            splitDataTuple = tuple(data[i].split(', '))
            dataList.append(splitDataTuple)
            syn, des, rate = dataList[i]
            for syntax in syntaxList:
                if syn in syntax and syn not in vulnerableSyntaxList:
                    vulnerableSyntaxList.append(syn)
                    vulnerableDescriptionList.append(des)
                    vulnerableRatingList.append(rate)
    return vulnerableSyntaxList, vulnerableDescriptionList, vulnerableRatingList


# Function to Show the Vulnerabilities in the Repo
def checkRepo(link, frame):
    vulSynList = list()
    vulDesList = list()
    vulRatingList = list()
    vulSynList, vulDesList, vulRatingList = returnVulnerable(link)

    # Clear the Frame
    clearFrame(frame)

    # Vertical Scrollbar
    verticalScrollBar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
    verticalScrollBar.grid(column=4, sticky='ns')

    # Text Box for Vulnerabilities
    textBox = tkinter.Text(frame, font=('Arial', 15), height=12, yscrollcommand=verticalScrollBar.set)
    textBox.insert(1.0, f'Following are the Vulnerabilities in the {link} Repo\n')
    textBox.insert(2.0, '\n')
    i = 3.0
    synMaxLength = len(max(vulSynList)) + 5
    desMaxLength = len(max(vulDesList)) + 5
    for index in range(len(vulSynList)):
        textBox.insert(i, f'{vulSynList[index]: >{synMaxLength}s}:-- {vulDesList[index]: ^{desMaxLength}s}\n')
        i = i + 1
    verticalScrollBar.config(command=textBox.yview)
    textBox.grid(row=0, columnspan=3, sticky='ns', padx=5, pady=5)

    # Rate Repo Button
    rateButton = tkinter.Button(frame, text='Rate Repo',
                                command=lambda: showRateButton(frame, vulRatingList))
    rateButton.grid(row=1, column=1, sticky='s')


# Function which show the Rating the for the Repo
def showRateButton(frame, ratingList):
    rate = 0.0
    for r in ratingList:
        rate = rate + int(r)
    rate = float(rate / len(ratingList))
    if rate == 0.0:
        rateLabel = tkinter.Label(frame, text="The Repo is safe and have Zero Vulnerabilities", font=('Arial', 20))
        rateLabel.grid()
    else:
        rateValue = (rate / 3.0) * 100
        lowerFrame = tkinter.Frame(frame)
        lowerFrame.grid(row=2, columnspan=3)

        # Rate Heading
        rateLabelHeading = tkinter.Label(lowerFrame, text="The Repo have Vulnerabilities", fg='red')
        rateLabelHeading.grid(row=0, column=0, sticky='n', columnspan=3)

        # Label to Show the rating
        rateLabel = tkinter.Label(lowerFrame, text=f'{rate:.3f}', fg='red')
        rateLabel.grid(row=1, columnspan=3)

        # Progress bar
        goodLabel = tkinter.Label(lowerFrame, text='Good: 0', fg='green')
        goodLabel.grid(row=2, column=0)
        progressBar = Progressbar(lowerFrame, orient=tkinter.HORIZONTAL, length=300, mode='determinate', value=rateValue)
        progressBar.grid(row=2, column=1, sticky='n')
        badLabel = tkinter.Label(lowerFrame, text='Bad: 3', fg='red')
        badLabel.grid(row=2, column=2)


# Function which calls the
def rateRepoBtn(link, frame):
    vul_syn_list, vul_des_list, vul_rating_list = returnVulnerable(link)
    clearFrame(frame)
    showRateButton(frame, vul_rating_list)


# Function to Display Team Information
def teamInfoDisplay(frame):
    clearFrame(frame)

    # Row Configure
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)

    # Column Configure
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)

    teamPost = tkinter.Label(frame, text='Team Member', font=('Arial', 15))
    teamPost.grid(column=0, row=0, sticky='n')
    memberName = tkinter.Label(frame, text='Name', font=('Arial', 15))
    memberName.grid(column=0, row=1, sticky='n')
    instituteName = tkinter.Label(frame, text='Institute Name', font=('Arial', 15))
    instituteName.grid(column=0, row=2, sticky='n')
    passingBatch = tkinter.Label(frame, text='Passing Batch', font=('Arial', 15))
    passingBatch.grid(column=0, row=3, sticky='n')

    # LEADER

    # Leader Label
    leaderLabel = tkinter.Label(frame, text='Leader', font=('Arial', 15))
    leaderLabel.grid(row=0, column=1, sticky='N')

    # Leader Name
    leaderName = tkinter.Label(frame, text="Aakash Raj", font=('Arial', 15))
    leaderName.grid(column=1, row=1, sticky='N')

    # Leader Institute Name
    leaderInstituteName = tkinter.Label(frame, text='Maharaja Agrasen Institute of\nof\nTechnology')
    leaderInstituteName.grid(column=1, row=2, sticky='N')

    # Leader Passing Batch
    leaderPassingBatchLabel = tkinter.Label(frame, text='2023', font=('Arial', 15))
    leaderPassingBatchLabel.grid(column=1, row=3, sticky='n')

    # Member-1

    # Member-1 Label
    memberOneLabel = tkinter.Label(frame, text='Member-1', font=('Arial', 15))
    memberOneLabel.grid(row=0, column=2, sticky='N')

    # Member-1 Name
    memberOneName = tkinter.Label(frame, text='Aniketh Varma', font=('Arial', 15))
    memberOneName.grid(row=1, column=2, sticky='n')

    # Member-1 Institute Name
    memberOneInstituteName = tkinter.Label(frame, text='Maharaja Agrasen Institute of\nof\nTechnology')
    memberOneInstituteName.grid(column=2, row=2, sticky='N')

    # Member-1 Passing Batch
    memberOnePassingBatchLabel = tkinter.Label(frame, text='2023', font=('Arial', 15))
    memberOnePassingBatchLabel.grid(column=2, row=3, sticky='n')

    # Member-2

    # Member-2 Label
    memberTwoLabel = tkinter.Label(frame, text='Member-2', font=('Arial', 15))
    memberTwoLabel.grid(row=0, column=3, sticky='N')

    # Member-2 Name
    memberTwoName = tkinter.Label(frame, text='Shrey Gupta', font=('Arial', 15))
    memberTwoName.grid(row=1, column=3, sticky='n')

    # Member-2 Institute Name
    memberTwoInstituteName = tkinter.Label(frame, text='Maharaja Agrasen Institute of\nof\nTechnology')
    memberTwoInstituteName.grid(column=3, row=2, sticky='N')

    # Member-2 Passing Batch
    memberTwoPassingBatch = tkinter.Label(frame, text='2023', font=('Arial', 15))
    memberTwoPassingBatch.grid(column=3, row=3, sticky='n')


def gui():
    def tempText(e):
        urlEntry.delete(0, "end")

    window = tkinter.Tk()
    window.title("Flipkart GRiD 4.0")

    # To find the center of the screen according to the app dimension
    appWidth = 1000
    appHeight = 750
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    centerWidth = int((screenWidth / 2) - (appWidth / 2))
    centerHeight = int((screenHeight / 2) - (appHeight / 2))

    # To give geometry to the app
    window.geometry(f'{appWidth}x{appHeight}+{centerWidth}+{centerHeight}')

    # Column width
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.columnconfigure(3, weight=1)

    # Row width
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    window.rowconfigure(5, weight=60)
    window.rowconfigure(6, weight=1)

    # Top Menu
    topMenuFrame = tkinter.Frame(window)
    topMenuFrame.grid(row=0, columnspan=3, sticky='N', pady=10, padx=10)

    # Display Frame
    displayFrame = tkinter.Frame(window)
    displayFrame.grid(row=5, columnspan=3, sticky='ns', padx=10, pady=10)

    # Label for team name Tech-junkies
    teamNameLabel = tkinter.Label(topMenuFrame, text="De-Sync", font=('Arial', 20))
    teamNameLabel.grid(columnspan=3, row=0, sticky="N", padx=5)

    # Image of team
    flipkartPic = Image.open('Images/De-Sync.png')
    flipkartPic = flipkartPic.resize((270, 150))
    flipkartPic = ImageTk.PhotoImage(flipkartPic)
    picLabel = tkinter.Label(topMenuFrame, image=flipkartPic)
    picLabel.image = flipkartPic
    picLabel.grid(row=1, columnspan=3)

    # URL Label
    urlLabel = tkinter.Label(topMenuFrame, text='GitHub Repo Link')
    urlLabel.grid(row=2, columnspan=3, sticky='ns')

    # URL
    inputRepoURL = tkinter.StringVar()
    urlEntry = tkinter.Entry(topMenuFrame, textvariable=inputRepoURL, width=60)
    urlEntry.insert(0, "Enter the GitHub URL of the Repo")
    urlEntry.grid(row=3, columnspan=3, sticky='ns')
    urlEntry.bind("<FocusIn>", tempText)
    urlEntry.update()

    # Buttons for Left Menu
    buttonWidth = 20
    buttonPadX = 5

    # Check Repo Button
    checkRepoButton = tkinter.Button(topMenuFrame, text="Check Repo", width=buttonWidth,
                                     command=lambda: checkRepo(inputRepoURL.get(), displayFrame))
    checkRepoButton.grid(row=4, column=0, padx=buttonPadX, pady=5)

    # Rate Repo Button
    rateRepoButton = tkinter.Button(topMenuFrame, text="Rate Repo", width=buttonWidth,
                                    command=lambda: rateRepoBtn(inputRepoURL.get(), displayFrame))
    rateRepoButton.grid(row=4, column=1, padx=buttonPadX, pady=5)

    # Display Code Button
    displayCodeButton = tkinter.Button(topMenuFrame, text="Display Codes", width=buttonWidth,
                                       command=lambda: displayCodesButton(inputRepoURL.get(), displayFrame))
    displayCodeButton.grid(row=4, column=2, padx=buttonPadX, pady=5)

    # Team Information Button
    teamInfo = tkinter.Button(window, text="Team Information", width=buttonWidth,
                              command=lambda: teamInfoDisplay(displayFrame))
    teamInfo.grid(row=6, column=0, padx=buttonPadX, pady=5)

    # Add Vulnerabilities Button
    addVulnerabilities = tkinter.Button(window, text=" Add Vulnerable Syntax", width=buttonWidth,
                                        command=lambda: addVulnerableSyntax(displayFrame))
    addVulnerabilities.grid(row=6, column=1, padx=buttonPadX, pady=5)

    # Close Button
    closeButton = tkinter.Button(window, text="Close", command=window.quit, width=buttonWidth)
    closeButton.grid(row=6, column=2, padx=20)

    window.mainloop()


gui()
