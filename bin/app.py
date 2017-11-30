import web
from sillywebgames import HPmap, piratemap

urls = (
    '/', 'Index',
    '/HPGame', 'HPGame',
    '/PirateGame', 'PirateGame',
    '/reset', 'reset'
)

app = web.application(urls, globals())

if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer = {'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base='layout')


class Index(object):

    def GET(self):
        return render.index()

    def POST(self):
        form = web.input()

        if form.game == "Harry Potter Game":
            game_map = HPmap
            session.room = game_map.begin
            web.seeother('/HPGame')
        elif form.game == "Pirate Game":
            game_map = piratemap
            session.room = game_map.begin
            web.seeother('/PirateGame')


class HPGame(object):

    def GET(self):
        if session.room:
            return render.hp_show_room(room=session.room)
        else:
            return render.you_failed()

    def POST(self):
        form = web.input(action=None)

        try:
            path = session.room.machinery(form.action)
            session.room = session.room.go(path)
        except:
            session.room = session.room.go('*')

        web.seeother("/HPGame")


class PirateGame(object):

    def GET(self):
        if session.room:
            return render.pir_show_room(room=session.room)
        else:
            return render.you_failed()

    def POST(self):
        form = web.input(action=None)

        try:
            path = session.room.machinery(form.action)
            session.room = session.room.go(path)
        except:
            session.room = session.room.go('*')

        web.seeother("/PirateGame")


class reset:

    def GET(self):
        session.kill()
        web.seeother('/')


if __name__ == "__main__":
    app.run()
