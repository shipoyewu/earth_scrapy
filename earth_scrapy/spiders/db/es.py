from elasticsearch import Elasticsearch as ES

class EsDao():
	
	conn = ES('cstor02:9200')

	def save(self, _index, _type, content):
		self.conn.index(index=_index, doc_type=_type, body=content)
		print "save.................."

