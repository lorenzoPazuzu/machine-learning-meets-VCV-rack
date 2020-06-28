from pydub import AudioSegment
from pydub.utils import make_chunks

VCV_audio = AudioSegment.from_file("ai_sounds-005.wav", "wav")
chunk_length_ms = 1000
chunks = make_chunks(VCV_audio, chunk_length_ms)

for i,chunk in enumerate(chunks):
    chunk_name = "patch{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")