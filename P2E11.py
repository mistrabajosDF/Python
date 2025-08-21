#procesar una lista de categorías para saber las subcategorías de cada una. 

import operator
categorias= """
Adaptive Technologies
Artistic Software
Communications

    BBS
    Chat
        ICQ
        Internet Relay Chat
        Unix Talk 
    Conferencing
    Email
        Address Book
        Email Clients (MUA)
        Filters
        Mail Transport Agents
        Mailing List Servers
        Post-Office
            IMAP
            POP3 
    FIDO
    Fax
    File Sharing
        Gnutella 
    Ham Radio
    Internet Phone
    Telephony
    Usenet News 

Database

    Database Engines/Servers
    Front-Ends 

Desktop Environment

    File Managers
    GNUstep
    Gnome
    K Desktop Environment (KDE)
    Screen Savers
    Window Managers
        Blackbox
        Fluxbox
        XFCE 

Documentation

    Sphinx 

Education

    Computer Aided Instruction (CAI)
    Testing 

Games/Entertainment

    Arcade
    Board Games
    First Person Shooters
    Fortune Cookies
    Multi-User Dungeons (MUD)
    Puzzle Games
    Real Time Strategy
    Role-Playing
    Side-Scrolling/Arcade Games
    Simulation
    Turn Based Strategy 

Home Automation
Internet

    File Transfer Protocol (FTP)
    Finger
    Log Analysis
    Name Service (DNS)
    Proxy Servers
    WAP
    WWW/HTTP
        Browsers
        Dynamic Content
            CGI Tools/Libraries
            Content Management System
            Message Boards
            News/Diary
            Page Counters
            Wiki 
        HTTP Servers
        Indexing/Search
        Session
        Site Management
            Link Checking 
        WSGI
            Application
            Middleware
            Server 
    XMPP
    Z39.50 

Multimedia

    Graphics
        3D Modeling
        3D Rendering
        Capture
            Digital Camera
            Scanners
            Screen Capture 
        Editors
            Raster-Based
            Vector-Based 
        Graphics Conversion
        Presentation
        Viewers 
    Sound/Audio
        Analysis
        CD Audio
            CD Playing
            CD Ripping
            CD Writing 
        Capture/Recording
        Conversion
        Editors
        MIDI
        Mixers
        Players
            MP3 
        Sound Synthesis
        Speech 
    Video
        Capture
        Conversion
        Display
        Non-Linear Editor 

Office/Business

    Financial
        Accounting
        Investment
        Point-Of-Sale
        Spreadsheet 
    Groupware
    News/Diary
    Office Suites
    Scheduling 

Other/Nonlisted Topic
Printing
Religion
Scientific/Engineering

    Artificial Intelligence
    Artificial Life
    Astronomy
    Atmospheric Science
    Bio-Informatics
    Chemistry
    Electronic Design Automation (EDA)
    GIS
    Human Machine Interfaces
    Hydrology
    Image Processing
    Image Recognition
    Information Analysis
    Interface Engine/Protocol Translator
    Mathematics
    Medical Science Apps.
    Physics
    Visualization 

Security

    Cryptography 

Sociology

    Genealogy
    History 

Software Development

    Assemblers
    Bug Tracking
    Build Tools
    Code Generators
    Compilers
    Debuggers
    Disassemblers
    Documentation
    Embedded Systems
    Internationalization
    Interpreters
    Libraries
        Application Frameworks
        Java Libraries
        PHP Classes
        Perl Modules
        Pike Modules
        Python Modules
        Ruby Modules
        Tcl Extensions
        pygame 
    Localization
    Object Brokering
        CORBA 
    Pre-processors
    Quality Assurance
    Testing
        Acceptance
        BDD
        Mocking
        Traffic Generation
        Unit 
    User Interfaces
    Version Control
        Bazaar
        CVS
        Git
        Mercurial
        RCS
        SCCS 
    Widget Sets 

System

    Archiving
        Backup
        Compression
        Mirroring
        Packaging 
    Benchmark
    Boot
        Init 
    Clustering
    Console Fonts
    Distributed Computing
    Emulators
    Filesystems
    Hardware
        Hardware Drivers
        Mainframes
        Symmetric Multi-processing
        Universal Serial Bus (USB) 
    Installation/Setup
    Logging
    Monitoring
    Networking
        Firewalls
        Monitoring
            Hardware Watchdog 
        Time Synchronization 
    Operating System
    Operating System Kernels
        BSD
        GNU Hurd
        Linux 
    Power (UPS)
    Recovery Tools
    Shells
    Software Distribution
    System Shells
    Systems Administration
        Authentication/Directory
            LDAP
            NIS 

Terminals

    Serial
    Telnet
    Terminal Emulators/X Terminals 

Text Editors

    Documentation
    Emacs
    Integrated Development Environments (IDE)
    Text Processing
    Word Processors 

Text Processing

    Filters
    Fonts
    General
    Indexing
    Linguistic
    Markup
        HTML
        LaTeX
        Markdown
        SGML
        VRML
        XML
        reStructuredText 

Utilities """

separo=categorias.split('\n')
lista_categorias={}
for linea in separo:
	if not len(linea)==0:
		if not linea.split(' ')[0]=='':		#Busca si el primer caracter es un espacio
			lista_categorias[linea]=[]				#Crea una clave con "linea" asociada a una lista vacia
			cat_actual=linea
		else:	
			lista_categorias[cat_actual].append(linea.strip())	

for key, value in sorted(lista_categorias.items(), key=operator.itemgetter(1)):
    print(f"{key}: {value}")

			
print ("\n=======================Otra version===================================\n")


categorias_dict = {}
cat_actual = None

for linea in categorias.splitlines():
    linea = linea.rstrip()
    if not linea:  # ignora líneas vacías
        continue
    if not linea.startswith(' '):  # categoría principal
        cat_actual = linea
        categorias_dict[cat_actual] = []
    else:  # subcategoría
        categorias_dict[cat_actual].append(linea.strip())

for cat, subcats in categorias_dict.items():
    print(f"{cat}: {len(subcats)} subcategorías -> {subcats}")

