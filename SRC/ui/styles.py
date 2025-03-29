# Estilos para la barra de herramientas
TOOLBAR_STYLE = """
    QToolBar { 
        background-color: #393E46; 
        color: white;
        spacing: 5px;
        padding: 3px;
    }
    
    QToolBar QToolButton { 
        /* Estilo base de botones */                                                                      
        padding: 3px;
        border-radius: 5px;
    }
    
    QToolButton:hover { 
        background-color: #1F4287 !important;                                     
    }
    
    QToolButton:checked { 
        background-color: #1F4287 !important;
        border-radius: 5px;
    }
    
    QToolBar::separator {
        background-color: #666666;
        width: 1px;
        margin: 4px 8px;
    }
"""


# Estilo para el contenedor principal
MAIN_CONTAINER_STYLE = "background-color: #606470;"

# Puedes agregar más estilos aquí
LABEL_STYLE = "color: white; font-size: 14px;"
TEXTFIELD_STYLE = "background-color: #444; color: white; border: 1px solid #666; border-radius: 3px; padding: 2px;"