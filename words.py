import random
from typing import Dict

from fastapi import APIRouter

import temp


words_router = APIRouter()


@words_router.get('/sentence')
def get_sentence() -> Dict:
    words = temp.words
    chosen = random.choice(words)
    sentence = chosen[0] + ' '

    for definition in chosen[1].get('definitions'):
        noun = definition.get('partOfSpeech', 'noun')
        worded_definition = definition.get('definition')
        sentence += f'({noun}) {worded_definition}. '

    sentence = sentence[:-2]
    return sentence
