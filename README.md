# WhatApp <=> Telegram Bridge

🆕  The written instructions can be found [here](http://ibcomputing.com/whatsapp-telegram-bridge/).

** LEGAL DISCLAIMER: ** It is possible that WhatsApp will end up blocking the phone number used to connect through yowsup-cli ** Use at your own Risk **

## License

This code is released under the MIT license (see LICENSE).

```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Example

[The LIVE unstable version of this Bot](https://blog.shrimadhavuk.me/posts/2017/12/31/Telegram-WhatApp/)

## How to set-up your own instance of this bot?

- ```cd $WORK_DIR```
- ```git clone git@github.com:SpEcHiDe/wat-bridge.git ```
- ```git clone git@github.com:AragurDEV/yowsup.git```
- ```virtualenv -p python3 venv```
- ```. venv/bin/activate```
- ```pip3 install -r requirements.txt```
- ```cd yowsup```
- ```python3 setup.py install```
- ```cd .. ```
- ```cd wat-bridge```
- ```mv development.conf config.conf```
- Edit config.conf according to the instructions given below.
- ```sh run.sh```
- ~sh status.sh~ This needs to be fixed. [Issue](https://github.com/SpEcHiDe/wat-bridge/issues/8)

## edit ```config.conf```

- The Telegram token is obtained by talking to the *BotFather* through Telegram and creating a bot, while the owner ID can be obtained by using the `/me` command.
- The database path is the full path to the file that will contain blacklist and contacts. Note that this path should be readable/writable by the user that executes the application.

### How to get yowsup-cli password?

```
yowsup-cli registration -r sms -m MCC -n MNC -C CC -p CCXXXXXXXXXX -E android
```

- Replace ```MCC```, ```MNC```, ```CC```, and ```CCXXXXXXXXXX``` as appropriate.

```
yowsup-cli registration -R CODE -m MCC -n MNC -C CC -p CCXXXXXXXXXX -E android
```

- Replace ```CODE``` with the WhatsApp verification code received, in the number that you had given.

### Extra Configuration (To Get the Log Files Delivered to your Telegram ChatBox)

- create a file named `UploadToTG.sh` with the following contents.

```
curl -i \
-F "chat_id={OWNER_CHAT_ID}" \
-F "document=@./log.txt" \
"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument"
```

- Replace the variables with your variables.

