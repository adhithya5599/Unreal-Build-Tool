@echo on
set FARMHANDSBUILDLOG=C:\Users\u1475663\source\repos\Unreal-Auto-Build\Temp\farmhandsbuild.log

echo [%date% %time%] Get the latest revision from perforce >> %FARMHANDSBUILDLOG% 2>&1
"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" "& 'C:\Program Files\Perforce\p4.exe' -c AdhithyaLab sync"
call "C:\Program Files\Epic Games\UE_5.6\Engine\Build\BatchFiles\Build.bat" -Target="FarmHandsEditor Win64 Development -Project=""C:\Users\u1475663\Perforce\AdhithyaLab\FarmHands.uproject""" -WaitMutex -NoHotReload
echo [%date% %time%] Latest Revision synced >> %FARMHANDSBUILDLOG% 2>&1

echo [%date% %time%] Starting Unreal Build Project Build >> %FARMHANDSBUILDLOG% 2>&1

set OUTDIR=C:\Users\u1475663\source\UnrealTestBuilds

if exist %OUTDIR% (
	echo [%date% %time%] Removing old build file >> %FARMHANDSBUILDLOG% 2>&1
	rmdir /s /q %OUTDIR%
)

echo [%date% %time%] Starting to build the project >> %FARMHANDSBUILDLOG% 2>&1
cmd.exe /c ^
""C:/Program Files/Epic Games/UE_5.6/Engine/Build/BatchFiles/RunUAT.bat" ^
  -ScriptsForProject="C:/Users/u1475663/Perforce/AdhithyaLab/FarmHands.uproject" ^
  Turnkey ^
    -command=VerifySdk ^
    -platform=Win64 ^
    -UpdateIfNeeded ^
    -EditorIO ^
    -EditorIOPort=49384 ^
    -project="C:/Users/u1475663/Perforce/AdhithyaLab/FarmHands.uproject" ^
  BuildCookRun ^
    -nop4 ^
    -utf8output ^
    -nocompileeditor ^
    -skipbuildeditor ^
    -cook ^
    -project="C:/Users/u1475663/Perforce/AdhithyaLab/FarmHands.uproject" ^
    -unrealexe="C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
    -platform=Win64 ^
    -installed ^
    -stage ^
    -package ^
    -build ^
    -pak ^
    -iostore ^
    -compressed ^
    -prereqs ^
	-archive ^
	-clientconfig=Development ^
    -nocompile ^
    -nocompileuat ^
    -archivedirectory="C:/Users/u1475663/source/UnrealTestBuilds" 
	
if exist %OUTDIR% (
	echo [%date% %time%] Farm Hands project was succesfully built >> %FARMHANDSBUILDLOG% 2>&1
)

echo [%date% %time%] Starting python script for Farm Hands Build upload to drive >> %FARMHANDSBUILDLOG% 2>&1
"C:\Program Files\Python313\python.exe" "C:\Users\u1475663\source\repos\Unreal-Auto-Build\app\fileUpload.py"
echo [%date% %time%] Finished uploading file to the drive >>%FARMHANDSBUILDLOG% 2>&1

echo [%date% %time%] Starting Unreal Build Discord bot >> %FARMHANDSBUILDLOG% 2>&1
"C:\Program Files\Python313\python.exe" "C:\Users\u1475663\source\repos\Unreal-Auto-Build\app\app.py"
echo [%date% %time%] Finished executing Unreal Build Discord bot >> %FARMHANDSBUILDLOG% 2>&1

exit