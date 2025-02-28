"""
Copyright (c) SIOS Technology, Inc. All rights reserved.

MIT License

text を読み込んで、content を チャンク分割するツール

usage: python split_txt.py textfilepath chunksize overlapsize

chunksize, overlapsize の単位は、文字数。（バイト数ではない。）
  -> 読み込み元の textfilepath と同じディレクトリ に分割後の txt が出力される。
"""

import re
import sys

from consts import DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP, MIN_CHUNK_SIZE, MIN_OVERLAP
from langchain.text_splitter import RecursiveCharacterTextSplitter


# chunk分割時のセパレーター
separators = ["\n\n", "\n", "」", "。", "）", "、", "，", " ", ""]


class JapaneseCharacterTextSplitter(RecursiveCharacterTextSplitter):
    """
    句読点も句切り文字に含めるようにするためのスプリッタ
    """

    def __init__(self, **kwargs):
        super().__init__(separators=separators, **kwargs)


def split_chunks(texts: str, chunk_size:int=DEFAULT_CHUNK_SIZE, chunk_overlap:int=DEFAULT_OVERLAP) -> list[str]:
    """
    指定されたサイズとオーバーラップでチャンク分割する。
    """
    text_splitter = JapaneseCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(texts)


def process1file(input_text_filename:str, output_json_filename:str, chunk_size:int, chunk_overlap:int):
    """
    1つのtextファイルに対して、解析、分割を行う。
    """

    all_contents :str = ""

    with open(file=input_text_filename, buffering=-1, encoding="utf-8") as input_file:
        while content := input_file.readline():

            # 改行しかない行は、いわば区切りのための行なので、そのままとしておく。
            if content != '\n':
                # 全角空白またはタブは半角空白に置換する。
                content = re.sub("[　\t]", " ", content)

                # 行頭の空白は削除する。
                content = re.sub(r"^[\s]+", "", content)

            all_contents += content

    # \s*\n\s+\n のような箇所は、\n\nでまとめる。
    all_contents = re.sub("\\s*\n\\s+\n", "\n\n", all_contents)

    # chunk 分割
    chunks: list[str] = split_chunks(all_contents, chunk_size, chunk_overlap)

    prev_line: str = ""

    # 分割処理しながら、チャンクを書き出す。
    with open(output_json_filename, "w", -1, "utf-8") as output_file:
        for i, chunk in enumerate(chunks):
            # chunk内の\nを""に置換する。
            chunk: str = chunk.replace("\n", "")

            if i == 0:
                # 先頭行は、読み込むだけとする。
                prev_line = chunk
                continue

            m = re.match(r"^([\s」。、，,）]+).*", chunk)

            if m:
                # 行の先頭に 」。、，,）が来ることがある。
                # 次の行の先頭が、」。、，,）だったら、前の行の末尾に移動させる。
                matched_str: str = m.group(1)

                prev_line += matched_str
                chunk = chunk[len(matched_str):]

                if chunk == "":
                    # 次の行が、空になった場合は、skip
                    continue

            output_file.write(f"{prev_line}\n")

            prev_line = chunk


        # 最終行の書き出し
        output_file.write(f"{prev_line}\n")


# ----- main -----
args: list[str] = sys.argv

text_filepath: str = args[1]

chunk_size: int = DEFAULT_CHUNK_SIZE
if len(args) > 2:
    chunk_size = int(args[2])
    if chunk_size < MIN_CHUNK_SIZE:
        chunk_size = MIN_CHUNK_SIZE

overlap_size: int = DEFAULT_OVERLAP
if len(args) > 4:
    overlap_size = int(args[3])
    if overlap_size < MIN_OVERLAP:
        overlap_size = MIN_OVERLAP

output_json_filepath: str = text_filepath + "_chunked.txt"

process1file(text_filepath, output_json_filepath, chunk_size, overlap_size)
