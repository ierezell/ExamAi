from settings import PAD_token
import torch
import itertools
from typing import List, Tuple


def zeroPadding(l: List[List[int]], fillvalue=PAD_token) -> List[List[int]]:
    """Convert list of list of ints to a matrix padded to get same dimmension

    Arguments:
        l {List[List[str]]} -- list of our senteces (with differents sizes)

    Keyword Arguments:
        fillvalue -- value to fill with (default: {PAD_token})

    Returns:
        list[list[int]] -- matrix with sentences padded
    """
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))


def maskMatrix(l: List[List[int]]) -> List[List[bool]]:
    """Gives the boolean matrix to know if element i,j is paddeding or not

    Arguments:
        l {List[List[str]]} -- list of our sentences converted first to ints

    Returns:
        List[List[bool]] -- matrix to know where padding is
    """
    mask = []
    for i, seq in enumerate(l):
        mask.append([])
        for token in seq:
            if token == PAD_token:
                mask[i].append(0)
            else:
                mask[i].append(1)
    return mask

# Returns padded input sequence tensor and lengths


def toInputTensor(voc, l: List[List[str]]):
    """Get list of sentences (list of words) and return a matrix with these
    sentences padded and converted to numbers. The fonction zeroPadding is
    applying a transpose !

    Arguments:
        voc {Voc} -- The class for our vocabulary
        l {List[List[str]]} -- list of sentences (list of words)

    Returns:
        padVar -- matrix with padded sentences converted to int
        lengths -- max length of the longest sentence in our list
    """
    indexes_batch = [voc.sentenceToIndex(sentence) for sentence in l]
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    padVar = torch.LongTensor(padList)
    return padVar, lengths

# Returns padded target sequence tensor, padding mask, and max target length


def toOutputTensor(voc, l: List[List[str]]):
    """Get list of sentences (list of words) and return a matrix with these
    sentences padded and converted to numbers. The fonction zeroPadding is
    applying a transpose !

    Arguments:
        voc {Voc} -- The class for our vocabulary
        l {List[List[str]]} -- list of sentences (list of words)

    Returns:
        padVar -- matrix with padded sentences converted to int
        mask -- matrix to know which element is padding
        max_target_len -- max length of the longest sentence in our list
    """
    indexes_batch = [voc.sentenceToIndex(sentence)
                     for sentence in l]
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    mask = maskMatrix(padList)
    mask = torch.ByteTensor(mask)
    padVar = torch.LongTensor(padList)
    return padVar, mask, max_target_len

# Returns all items for a given batch of pairs


def batch2TrainData(voc, pair_batch: List[Tuple[List[str], List[str]]]):
    """Take batch of pairs sentence and return them in a good format
    (matrix of numbers padded)

    ex : [("Hello how are you ?", "I'm good thanks"),
            ("You're stupid","thanks")]
        =>
        inp = [[564, 45, 82, 123],
                [46, 123, 0, 0]]
        length = [4, 2]
        output = [[357,195,65],
                    [889, 0, 0]]
        mask = [[1,1,1],
                [1, 0, 0]]
        max_target_length = 3

    Arguments:
        voc -- Instance of the Voc class
        pair_batch {List[Tuple[List[str], List[str]]]} -- list of the pairs of
                                                            dialog

    Returns:
        inp -- 2D Tensor with the int matrix of input sentences,
                organized by batch
        lengths -- 1D Tensor with lenght of each input sentence
        output -- 2D Tensor with the int matrix of output senteces,
                    organized by batch
        mask -- 2D Tensor with the bool matrix which tell where is the padding
        max_target_len -- int to give output sentence maximal length
    """
    pair_batch.sort(key=lambda x: len(x[0]), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
    inputTensor, lengths = toInputTensor(voc, input_batch)
    outputTensor, mask, max_target_len = toOutputTensor(voc, output_batch)
    return inputTensor, lengths, outputTensor, mask, max_target_len
