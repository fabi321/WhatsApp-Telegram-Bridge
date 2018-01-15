# wat-bridge

## NEW

The written instructions can be found [here](http://ibcomputing.com/whatsapp-telegram-bridge/).

A bridge between WhatsApp and Telegram.

This creates two listeners, one for WhatsApp and another for a Telegram bot. 

**IMPORTANT WARNING:** it is possible that WhatApp will end up blocking the phone number used to connect through yowsup, **use at your own risk**.

## Usage

```
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ sh run.sh
$ sh status.sh
```

**NOTE:** For some reason, yowsup has issues when receiving messages. The workaround mentioned at <https://github.com/tgalal/yowsup/issues/1613#issuecomment-247801568> works, so instead of installing yowsup from requirements, use:

```
$ pip install git+https://github.com/AragurDEV/yowsup.git
```

## Configuration

```conf
[tg]
owner = ONWER_ID
token = TOKEN

[wa]
phone = PHONE_NUMBER
password = PASSWORD

[db]
path = PATH_TO_DB
```

The Telegram token is obtained by talking to the *BotFather* through Telegram and creating a bot, while the owner ID can be obtained by using the `/me` command.

The WhatsApp phone must include the country code (without any additional characters such as `+`, only the digits) followed by the number, for instance `49xxxxxxxxx`, and the password can be obtained through the [Yowsup cli interface](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0).

Lastly, the database path is the full path to the file that will contain blacklist and contacts. Note that this path should be readable/writable by the user that executes the application.

## How to get yowsup-cli password?

```
yowsup-cli registration -r sms -m MCC -n MNC -C CC -p CCXXXXXXXXXX -E android
```

- Replace ```MCC```, ```MNC```, ```CC```, and ```CCXXXXXXXXXX``` as appropriate.

```
yowsup-cli registration -R CODE -m MCC -n MNC -C CC -p CCXXXXXXXXXX -E android
```

- Replace ```CODE``` with the WhatsApp verification code received, in the number that you had given.

## Example

[The LIVE unstable version of this Bot](https://t.me/WhatAppStatus)

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
