import re
import uuid

from config import Config


class ReferralLink:
    REGEXP_PATTERN = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"

    @classmethod
    def search_ref_code(cls, text: str):
        regexp = re.compile(cls.REGEXP_PATTERN)
        ref_code = regexp.findall(text)
        return ref_code[0] if len(ref_code) else ""

    @classmethod
    def generate_ref_code(cls):
        return str(uuid.uuid4())

    @classmethod
    def generate_ref_link(cls, ref_code: str):
        return 'https://t.me/{}?start={}'.format(Config.BOT_URL, ref_code)



if __name__ == '__main__':
    ref_code = ReferralLink.generate_ref_code()
    print(ReferralLink.generate_ref_link(ref_code))
    print(ReferralLink.search_ref_code("/start ca3ed6dc-3b29-4192-9e98-338232f1c392"))
    print(len(ReferralLink.search_ref_code("/start ca3ed6dc-3b29-4192-9e98-338232f1c392")))
