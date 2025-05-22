###### ------- Iris ------- ######
#### --- Project Overview --- ####

# Features
-User Authentication{
-username
-password(getpass)
}


EXAMPLE DEPENDENCY CHAIN 
main.py    # launches iris
└──> core.py   # decides *how* to launch iris, eventually performing system hardware checks to determine what "model mode"  (ex: --lazy_submodel) to run, as well as model capabilities
     └──> (CLI mode) cli/main.py
             └──> model_manager.py     #loads models
            └──> memory_framework.py   #memory management
             └──> user.py              #user and session authentication
             └──> routing.py           #directing prompts to each model
     └──> (GUI mode) gui/qt_app.py
             └──> model_manager.py  
             └──> memory_framework.py
             └──> user.py
             └──> routing.py

if --lazy_submodel is enabled, the subconscious model (pixtral-12b) will be disabled at start - allowing for only on-demand usage (like in deep reflections and deep-think tasks)
    -without this flag, both models are loaded at start; giving iris the ability to choose when to process information with the subconscious - as well as a deeper access to the entire memory bank (fully located and utilized with the sub model)
    -the main conscious model (mixtral 7b instruct) primarily has a context of the current user and session, while it's ability to deeply think/access its entire memory bank relies on the subconscious model; imitating the separation between the conscious and subconscious mind.

