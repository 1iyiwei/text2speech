Const SAFT48kHz16BitStereo = 39
Const SSFMCreateForWrite = 3 ' Creates file even if file exists and so destroys or overwrites the existing file

If WScript.Arguments.Count <> 2 Then
    WScript.Echo "Usage: cscript speech.vbs inputTextFile outputWavFile"
    WScript.Quit
End If

Dim oFileStream, oVoice

voicePath = Wscript.Arguments.Item(0)

voiceString =  CreateObject("Scripting.FileSystemObject").OpenTextFile(voicePath, 1).ReadAll()

Set oFileStream = CreateObject("SAPI.SpFileStream")
oFileStream.Format.Type = SAFT48kHz16BitStereo
oFileStream.Open Wscript.Arguments.Item(1) , SSFMCreateForWrite

Set oVoice = CreateObject("SAPI.SpVoice")
Set oVoice.AudioOutputStream = oFileStream
oVoice.Speak voiceString

oFileStream.Close