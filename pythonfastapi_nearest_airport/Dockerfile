FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Update the Python version and URL here if 3.13.3 is available
RUN powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe -OutFile python-installer.exe ; \
    Start-Process python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_test=0' -NoNewWindow -Wait ; \
    Remove-Item -Force python-installer.exe"

WORKDIR C:/app

#COPY main.py .
#COPY requirement.txt .
#COPY *.sav ./
#COPY web.config .

COPY . .

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 443

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "wildcard_tridiondemo_com.key.pem", "--ssl-certfile", "wildcard_tridiondemo_com.crt.pem"]