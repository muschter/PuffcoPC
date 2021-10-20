# import compiled qt resource data

__import__('resources')

if __name__ == "__main__":
    from asyncio import ensure_future, get_event_loop, sleep
    from PyQt5.QtGui import QFont, QFontDatabase
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    QFontDatabase.addApplicationFont(':/fonts/assets/puffco-slick.ttf')
    app.setFont(QFont('Slick'))

    main_loop = get_event_loop()

    from puffco.ui import PuffcoMain
    ui = PuffcoMain('84:2E:14:80:2B:5A', main_loop)

    async def _process():
        # replacement for app._exec, allowing us to use
        # asyncio's event loops to update the UI
        while True:
            app.processEvents()
            await sleep(0)

    _process_task = ensure_future(_process())
    _connect_task = ensure_future(ui.connect(), loop=main_loop)
    ui.show()
    try:
        main_loop.run_forever()
        # sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
    finally:
        _process_task.cancel()
        _connect_task.cancel()
        app.quit()