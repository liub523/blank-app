import streamlit as st

# 设置页面标题
st.title("ST2110-20 SDP ")

# 调整左侧参数区域的宽度
st.sidebar.header("Parameter Settings")
media_name = st.sidebar.text_input("Media Name", "example_media")
media_type = st.sidebar.selectbox("Media Type", ["Video", "Audio"])

if media_type == "Video":
    st.sidebar.subheader("Video Settings")
    col1, col2, col3 = st.sidebar.columns(3)  # 创建三列布局
    with col1:
        video_codec = st.selectbox("Video Codec", ["H264", "H265", "JPEG2000"])
        width = st.number_input("Width", min_value=1, value=1280)
        sampling = st.selectbox("Sampling", ["YCbCr-4:2:0", "YCbCr-4:2:2", "YCbCr-4:4:4"])
    
    with col2:
        height = st.number_input("Height", min_value=1, value=720)
        framerate = st.number_input("Framerate", min_value=1, value=60000)
    
    with col3:
        depth = st.selectbox("Depth", ["8", "10", "12"])
        colorimetry = st.selectbox("Colorimetry", ["BT.601", "BT.709", "BT.2020"])
        tcs = st.selectbox("TCS", ["SDR", "HDR10", "HLG"])
    
    port = st.sidebar.number_input("Video Port", min_value=1024, max_value=65535, value=30000)
    
    media_type_str = f"video {port} RTP/AVP 96"
    fmtp_str = f"sampling={sampling}; width={width}; height={height}; exactframerate={framerate}/1001; depth={depth}; TCS={tcs}; colorimetry={colorimetry}"
else:
    st.sidebar.subheader("Audio Settings")
    col1, col2, col3 = st.sidebar.columns(3)  # 创建三列布局
    with col1:
        audio_codec = st.selectbox("Audio Codec", ["AAC", "PCM", "MP2T"])
        sample_rate = st.number_input("Sample Rate", min_value=8000, value=48000)
    
    with col2:
        channels = st.number_input("Channels", min_value=1, value=2)
        bit_depth = st.selectbox("Bit Depth", [16, 24])
    
    with col3:
        sampling = st.selectbox("Sampling", ["1", "2", "3", "4"])
        depth = st.selectbox("Depth", ["16", "24"])
    
    port = st.sidebar.number_input("Audio Port", min_value=1024, max_value=65535, value=5000)
    
    media_type_str = f"audio {port} RTP/AVP 96"
    fmtp_str = f"sample_rate={sample_rate}; channels={channels}; bit_depth={bit_depth}; sampling={sampling}; depth={depth}"

ip_address = st.sidebar.text_input("IP Address", "192.168.1.1")
sdp_version = st.sidebar.number_input("SDP Version", min_value=0, value=0)

# 生成 SDP 文本
sdp_text = f"""v=0
o=- 0 0 IN IP4 {ip_address}
s={media_name}
c=IN IP4 {ip_address}
t=0 0
a=tool:libavformat 58.29.100
m={media_type_str}
a=rtpmap:96 {video_codec if media_type == "Video" else audio_codec}/90000
a=fmtp:96 {fmtp_str}
a=recvonly
"""

# 右侧显示生成的 SDP 文本，使用 st.text_area 以支持自动换行
st.header("Generated SDP Text")
st.text_area("SDP Output", value=sdp_text, height=300, disabled=True)  # 设置高度以支持自动换行
