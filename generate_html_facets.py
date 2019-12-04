import argparse
import pandas as pd
import os
import sys
import base64
from facets_overview.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator


class OpenFile:
    """
    Class that open a file and close it at the end

    Attributes
    ----------
    fname : str
        file name
    mode : str
        mode for open() method
    """

    def __init__(self, fname: str, mode='r'):
        self.fname = fname
        self.mode = mode

    def __enter__(self):
        self.file = open(self.fname, self.mode)
        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()


def str_to_file(string: str, fname: str):
    """
    Create a file based on a string.

    Parameters
    ----------
    string: str
        string to write into the file
    fname: str
        file name
    """
    fpath = os.getcwd() + '/' + fname

    with OpenFile(fpath, 'w') as file:
        file.write(string)
    file.close()
    print('File created at ', fpath)


def generate_facets_dive_html(data: pd.DataFrame):
    jsonstr = data.to_json(orient='records')
    HTML_TEMPLATE = """
            <script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
            <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">
            <facets-dive id="elem" height="600"></facets-dive>
            <script>
            var data = {jsonstr};
            document.querySelector("#elem").data = data;
            </script>"""
    html = HTML_TEMPLATE.format(jsonstr=jsonstr)
    return html

def generate_facets_overview_html(proto_list: list):
    gfsg = GenericFeatureStatisticsGenerator()        
    proto = gfsg.ProtoFromDataFrames(proto_list)
    protostr = base64.b64encode(proto.SerializeToString()).decode("utf-8")

    HTML_TEMPLATE = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
    <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html" >
    <facets-overview id="elem"></facets-overview>
    <script>
        document.querySelector("#elem").protoInput = "{protostr}";
    </script>"""
    html = HTML_TEMPLATE.format(protostr=protostr)
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="path to csv data")
    parser.add_argument("--type", help="type of facets generation : dive or overview", default="dive")
    parser.add_argument("--output", help="path and file name where the html will be stored", default="output/facets.html")
    parser.add_argument("--target", help="target column to split your data for overview ", default=None)
    args = parser.parse_args()

    if args.output[-5:] != '.html':
        raise Exception('output file needs to be an html file : file.html') 

    data = pd.read_csv(args.data)

    if args.type == 'dive':
        html = generate_facets_dive_html(data)
    else:
        proto_list = list()
        if type(args.target) == type(None):
            proto_list.append({'name': 'data', 'table': data})
        else:
            if args.target not in data.columns:
                raise Exception('target column not in data') 

            for unique_val in data[args.target].unique():
                filter_data = data[data[args.target] == unique_val]
                proto_list.append({'name': unique_val, 'table': filter_data})
            del filter_data

        html = generate_facets_overview_html(proto_list)

    fname = args.output
    str_to_file(html, fname=fname)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
