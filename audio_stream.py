def stream_audio(p, chunk, job):
    wf = wave.open(job, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    while data != b'':
        print(calculate_position_percent(wf.tell(), wf.getnframes()))
        stream.write(data)
        data = wf.readframes(chunk)

    # Check queue and load next element

    # stop stream (6)
    stream.stop_stream()
    stream.close()
    wf.close()
    return True


def check_audio_device(p):
    p.get_default_output_device_info()
    device_count = p.get_device_count()

    for i in range(0, device_count):
        yield p.get_device_info_by_index(i)["name"],p.get_device_info_by_index(i)["index"]


