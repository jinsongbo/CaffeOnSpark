from PIL import Image
from io import BytesIO
from IPython.display import HTML
import numpy as np
from base64 import b64encode
from google.protobuf import text_format

import caffe
import caffe.draw
from caffe.proto import caffe_pb2

def get_np_array(row):
    return np.frombuffer(row.data, 'uint8').reshape((row.height,row.width))

def image_tag(np_array): 
    im = Image.fromarray(np_array, 'L')
    bytebuffer = BytesIO()
    im.save(bytebuffer, format='png')
    return "<img src='data:image/png;base64," + b64encode(bytebuffer.getvalue()) + "' />"

def show_df(df, nrows=10):
    data = df.take(nrows)
    html = "<table><tr><th>Index</th><th>Label</th><th>Image</th>"
    for i in range(nrows):
        row = data[i]
        html += "<tr>"
        html += "<td>%s</td>" % row.id
        html += "<td>%s</td>" % row.label
        html += "<td>%s</td>" % image_tag(get_np_array(row))
        html += "</tr>"
    html += "</table>"
    return HTML(html)

def show_network(input_net_proto_file, rankdir):
    net = caffe_pb2.NetParameter()
    text_format.Merge(open(input_net_proto_file).read(), net)
    image=caffe.draw.draw_net(net, rankdir)
    html = "<body>"
    html += "<img src='data:image/png;base64," + b64encode(image) + "' />"
    html += "</body>"
    return HTML(html)
    
