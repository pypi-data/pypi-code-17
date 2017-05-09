from ppg_common.clients.base import BaseClient


class PandoraClient(BaseClient):
    urls = {
        'create_box': '/v1/box',
        'box': '/v1/box/{}',
        'files': '/v1/files/{}'
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(PandoraClient, self).__init__(host, port, ssl, session)

    def create_box(self, box_name):
        query_box_url = self.urls.get('create_box')
        return self.post(query_box_url, body={}, query="name={}".format(
            box_name))

    def list_box(self, box_id):
        return self.get(self.urls.get("box").format(box_id))

    def delete_box(self, box_id):
        return self.delete(self.urls.get("box").format(box_id))

    def list_by_query(self, box_id, inquiry):
        url = self.urls.get("box").format(box_id)
        return self.get(url, query="inquiry={}".format(inquiry))

    def update_by_query(self, box_id, inquiry, tag_name, tag_value):
        url = self.urls.get("box").format(box_id)
        return self.patch(url,
                          query="inquiry={}&tag-name={}&tag-value={}".format(
                              inquiry, tag_name, tag_value))

    def delete_by_query(self, box_id, inquiry):
        url = self.urls.get("box").format(box_id)
        return self.delete(url, query="inquiry={}".format(inquiry))

    def upload_file(self, box_id, file_name, uploaded_input_stream):
        query_params = "?boxID=" + box_id + "&name=" + file_name
        url = '/files'
        return self.post(url, query="boxID={}&name={}".format(box_id,
                                                              file_name))

    def download_file(self, file_id):
        url = self.urls.get("files").format(file_id)
        return self.get(url)

    def delete_file(self, file_id):
        url = self.urls.get("files").format(file_id)
        return self.delete(url)

    def copy_file(self, file_id, name, box_id):
        url = self.urls.get("files").format(file_id) + "/copy"
        return self.get(url, quert="boxID={}&name={}".format(box_id, name))

    def get_info(self, file_id):
        url = self.urls.get("files").format(file_id) + "/info"
        return self.get(url)

    def add_tag(self, file_id, tag_name, tag_value):
        query_params = "?tag-name=" + tag_name + "&tag-value=" + tag_value
        url = self.urls.get("files").format(file_id) + "/tag"
        return self.post(url, query="tag-name={}&tag-value={}".format(
            tag_name, tag_value))

    def delete_tag(self, file_id, tag_name, tag_value):
        url = self.urls.get("files").format(file_id) + "/tag"
        return self.post(url, query="tag-name={}&tag-value={}".format(
            tag_name, tag_value))



