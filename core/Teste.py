from imdb import IMDb

class get_imdb():

	def get_movie(self, id:str):
		data = []
		movie = IMDb()
		filme = movie.get_movie(id) #without 'tt'

		print('name:', filme['localized title'])
		print('cover:', filme['full-size cover url'])
		print('plot:', filme['plot'])

#		return data