QT += widgets
#requires(qtConfig(combobox))


HEADERS       = renderarea.h \
                window.h
SOURCES       = main.cpp \
                renderarea.cpp \
                window.cpp
RESOURCES     = lidar.qrc

unix {
    LIBS += -lboost_system
}


# install
#target.path = $$[QT_INSTALL_EXAMPLES]/widgets/painting/basicdrawing
#INSTALLS += target
