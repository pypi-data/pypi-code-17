import bonobo

from bonobo.ext.opendatasoft import OpenDataSoftAPI

registration_datasets = [
    'entreprises-immatriculees-2012',
    'entreprises-immatriculees-2013',
    'entreprises-immatriculees-2014',
    'entreprises-immatriculees-2015',
    'entreprises-immatriculees-2016',
    'entreprises-immatriculees-2017',
]

graph = bonobo.Graph(
    OpenDataSoftAPI(dataset=registration_datasets[0], netloc='datainfogreffe.fr', rows=10, limit=25),
    bonobo.PrettyPrint(title_keys=('denomination', )),
    bonobo.count,
    bonobo.PrettyPrint(),
)

if __name__ == '__main__':
    bonobo.run(graph)
