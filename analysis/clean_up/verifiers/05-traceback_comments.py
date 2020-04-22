import praw, json, datetime, time

from praw import models

to_be_fixed = """2020-03-25 04:01:51.464937	u/Cool_Mayonaise	flfyu2l	u/kink_creamson	flfyo60	C infected by someone not already infected
2020-03-25 04:02:22.084620	u/tfcuber101	flfyuvi	u/Yusuri-San	flfyriw	C infected by someone not already infected
2020-03-25 04:03:46.165811	u/tshax	flfyx81	u/jospehjoestar	flfyvgy	C infected by someone not already infected
2020-03-25 04:04:37.436807	u/PrideInModesty	flfyyin	u/jospehjoestar	flfyvgy	C infected by someone not already infected
2020-03-25 04:05:58.441463	u/finn_ruttchen	flfz12e	u/kink_creamson	flfv3qi	C infected by someone not already infected
2020-03-25 04:12:23.831106	u/buckeyefire	flfzcnx	u/Chong_Long_Dong	fomjx0	S infected by someone not already infected
2020-03-25 04:13:35.941845	u/schloooooooop	flfze14	u/neopolitam	flfyftz	C infected by someone not already infected
2020-03-25 04:19:21.330793	u/phoenix_is_gay	flfznfz	u/Anoobis100percent	flfxjzj	C infected by someone not already infected
2020-03-25 04:39:44.248171	u/serial_code_r	flg0lbw	u/ItsSynnoX	flfykxo	C infected by someone not already infected
2020-03-25 04:44:45.663050	u/7H3_D31M0S	flg0ttb	u/UnKnOwNLIKER	flfya2l	C infected by someone not already infected
2020-03-25 04:47:21.692608	u/Wanking_the_dog	flg0yyh	u/BeardPhile	flfyhrd	C infected by someone not already infected
2020-03-25 04:48:11.245121	u/Endrelish	flg10uj	u/not-a-Shrek	flfs3fd	C infected by someone not already infected
2020-03-25 05:00:08.523734	u/AutomatedKiwi	flg1ocp	u/Yusuri-San	flfv8hq	C infected by someone not already infected
2020-03-25 05:06:49.278268	u/_Xystus69	flg1zo0	u/_TheRope	flfxlyo	C infected by someone not already infected
2020-03-25 05:13:21.275604	u/awopolo	flg2bl2	u/Sex_Shop_Souvenir	flfy8vm	C infected by someone not already infected
2020-03-25 05:16:25.860293	u/Akysh96	flg2fuc	u/Uncle_Freddy	flfyjua	C infected by someone not already infected
2020-03-25 05:19:55.674974	u/Wicked_one911	flg2n6l	u/LeonidtheWill	flfxyps	C infected by someone not already infected
2020-03-25 05:21:13.661473	u/AureusD	flg2p28	u/jospehjoestar	flg2n7k	C infected by someone not already infected
2020-03-25 05:25:08.699692	u/josh3169	flg2uy6	u/jospehjoestar	flg2n7k	C infected by someone not already infected
2020-03-25 05:28:29.292408	u/Gamer_Tn_XD	flg30lf	u/kink_creamson	flg1xae	C infected by someone not already infected
2020-03-25 05:38:25.866585	u/TheRealBluefire	flg3j8w	u/not-a-Shrek	flfs3fd	C infected by someone not already infected
2020-03-25 05:42:11.393954	u/Calvincake911meme	flg3qe8	u/NotFunnyBuddy	flfwjng	C infected by someone not already infected
2020-03-25 06:09:39.466524	u/KingBradleyWrath	flg4z5v	u/Yusuri-San	flfv8hq	C infected by someone not already infected
2020-03-25 06:52:32.342744	u/Damiioblivion	flg6ydv	u/Yusuri-San	flfidno	C infected by someone not already infected
2020-03-25 07:00:36.986681	u/cs_sf	flg7cnj	u/Chong_Long_Dong	flfylxo	C infected by someone not already infected
2020-03-25 07:03:54.575633	u/Normankoailey	flg7hj2	u/ItsSynnoX	flfykxo	C infected by someone not already infected
2020-03-25 07:34:35.605578	u/amberpudding	flg8z9g	u/ItsSynnoX	flfykxo	C infected by someone not already infected
2020-03-25 07:48:03.744837	u/DerpiDude1337	flg9p8b	u/Yusuri-San	flfv8hq	C infected by someone not already infected
2020-03-25 08:07:23.767547	u/caleb0923	flgatmi	u/Yusuri-San	flfidno	C infected by someone not already infected
2020-03-25 08:18:40.034725	u/aslappyboi	flgbltw	u/GloryToDucks39	flfvfmp	C infected by someone not already infected
2020-03-25 09:07:29.025597	u/ParryThisCasualFilth	flget1m	u/UnKnOwNLIKER	flfya2l	C infected by someone not already infected
2020-03-25 09:45:45.846567	u/gastergofaster	flgikzt	u/not-a-Shrek	flfs3fd	C infected by someone not already infected
2020-03-25 10:39:58.504683	u/Allata	flgnywz	u/my-name-is-blank	flgmxk3	C infected by someone not already infected
2020-03-25 13:30:43.952444	u/Potatoboiftw	flh6y8r	u/5amukai	flgl4zu	C infected by someone not already infected
2020-03-25 13:46:52.756322	u/keybored12	flh81xh	u/spiritually_deceased	flftlwu	C infected by someone not already infected
2020-03-25 14:31:15.893919	u/kidzwithkatz	flhe25f	u/5amukai	flgl4zu	C infected by someone not already infected
2020-03-25 14:49:21.445268	u/d_e_l_i_r_i_o_u_s	flhfavg	u/skootus	flfylqx	C infected by someone not already infected
2020-03-25 16:38:35.414914	u/scooter--ankle	flhrinm	u/TerryBlue2	flhr7gv	C infected by someone not already infected
2020-03-25 20:45:15.791816	u/StillShadows2	flihzrw	u/theMeatman7	flih2of	C infected by someone not already infected
2020-03-25 21:13:29.844483	u/Rochard11	flikmmw	u/my-name-is-blank	fli1stu	C infected by someone not already infected
2020-03-25 23:49:25.033121	u/Turtenguin	fliyxu5	u/my-name-is-blank	fli1stu	C infected by someone not already infected
2020-03-26 00:59:56.923431	u/dr-karate	flj4dfd	u/Sour_Gamer	flio2am	C infected by someone not already infected
2020-03-26 03:53:31.795881	u/TREX2069	fljdxw7	u/my-name-is-blank	fljczlt	C infected by someone not already infected
2020-03-26 11:48:37.906421	u/ROOBIT_2	flkabgw	u/ItsSynnoX	flka8vk	C infected by someone not already infected
2020-03-27 02:58:59.255938	u/JakeStuder1	flmpv5i	u/ItsSynnoX	fpl7xo	S infected by someone not already infected
2020-03-27 12:02:12.764723	u/rsfct_495	flnrab9	u/Scarecrow_1912	flnldlw	C infected by someone not already infected
2020-03-27 12:09:55.607780	u/stark2op	flnrsfi	u/Scarecrow_1912	flnrkle	C infected by someone not already infected
2020-03-27 12:47:47.637799	u/Oligarchic_Olive	flnx6zz	u/ItsSynnoX	flmnvyp	C infected by someone not already infected
2020-03-27 22:39:23.272122	u/Sam-Mufale	flpm46i	u/ItsSynnoX	flpec5h	C infected by someone not already infected
2020-03-28 15:13:33.583876	u/riceforme	flrkm7w	u/GloryToDucks39	flrk0v4	C infected by someone not already infected
2020-03-28 15:20:26.866540	u/L0raz-Thou-R0c0n0	flrm658	u/GloryToDucks39	flrk0v4	C infected by someone not already infected
2020-03-28 16:33:30.144163	u/L0rak0	flrsgy9	u/GloryToDucks39	flrj0s7	C infected by someone not already infected
2020-03-28 18:34:27.202840	u/TheDankDiamond	fls4ghj	u/GloryToDucks39	flrk0v4	C infected by someone not already infected
2020-03-28 19:18:21.436631	u/Socialanxietypigeon	fls9p3p	u/GloryToDucks39	flrk0v4	C infected by someone not already infected
2020-03-28 21:15:13.052693	u/palapenguin	flsk2mb	u/theMeatman7	flsjyov	C infected by someone not already infected
2020-03-28 21:16:31.061780	u/Lurgz_Lair	flsk5fd	u/theMeatman7	flsjyov	C infected by someone not already infected
2020-03-28 23:11:19.199603	u/Rking_9516	flsuj26	u/theMeatman7	flsuefd	C infected by someone not already infected
2020-03-29 01:21:47.717276	u/JintalJortail	flt4t00	u/theMeatman7	flt2twh	C infected by someone not already infected
2020-03-29 02:33:40.758445	u/_bustercherry_	flt99iy	u/theMeatman7	flsrkkh	C infected by someone not already infected
2020-03-29 07:01:29.871998	u/WatchWill	fltmpvy	u/theMeatman7	fltlrgd	C infected by someone not already infected
2020-03-29 09:35:36.634721	u/guffy000	fltvvkg	u/theMeatman7	fltgrzz	C infected by someone not already infected
2020-03-29 11:43:48.313771	u/rafaelloBonParrt	flu6vzy	u/theMeatman7	fltgrzz	C infected by someone not already infected
2020-03-29 12:13:46.619203	u/b2theherb	flu8qg2	u/UnKnOwNLIKER	flu4tq2	C infected by someone not already infected
2020-03-30 05:27:40.645529	u/blu-mister	flwplmw	u/Chong_Long_Dong	flwjquv	C infected by someone not already infected
2020-03-30 15:55:44.338345	u/zorrozwoelf	fly9jhe	u/theMeatman7	fly9d5j	C infected by someone not already infected
2020-03-30 15:59:50.976933	u/jkullberg93	fly9twa	u/theMeatman7	fly9d5j	C infected by someone not already infected
2020-03-30 22:26:48.741563	u/AlphaMari0	flzcy9t	u/theMeatman7	flzcs8d	C infected by someone not already infected
2020-03-31 00:50:32.995507	u/Rugs711	flzq5ax	u/theMeatman7	flzq3z0	C infected by someone not already infected
2020-03-31 02:17:49.230598	u/mcLordButt	flzvyfs	u/theMeatman7	flzvwps	C infected by someone not already infected
2020-03-31 05:02:40.911677	u/timmyoes	fm053pb	u/Chong_Long_Dong	fm04uyz	C infected by someone not already infected
2020-03-31 05:27:45.346881	u/itsmeyourfuhrer	fm06dxg	u/Chong_Long_Dong	fm06d5p	C infected by someone not already infected
2020-03-31 06:21:43.639065	u/fartsneef	fm08uxs	u/Chong_Long_Dong	fm04ypo	C infected by someone not already infected
2020-03-31 06:51:40.647446	u/leisim17	fm0ab2n	u/Chong_Long_Dong	fm04ypo	C infected by someone not already infected
2020-03-31 07:27:59.892146	u/dev_ya_boi	fm0d1js	u/Anoobis100percent	fm08pxe	C infected by someone not already infected
2020-03-31 09:36:10.921546	u/Poacatat	fm0m863	u/Chong_Long_Dong	fm04ypo	C infected by someone not already infected
2020-03-31 16:06:37.936667	u/Lixlo	fm1tj7x	u/theMeatman7	fm1tdb9	C infected by someone not already infected
2020-03-31 17:17:28.135370	u/Marce5002	fm2162v	u/theMeatman7	fm2126i	C infected by someone not already infected
2020-03-31 18:46:21.299589	u/IhadFun1time	fm2bq68	u/theMeatman7	fm26n9w	C infected by someone not already infected
2020-03-31 18:49:40.041467	u/jacket_with_sleeves	fm2c285	u/theMeatman7	fm28lzs	C infected by someone not already infected
2020-03-31 18:54:50.533908	u/PermanenttanCanada	fm2cg06	u/theMeatman7	fm21tc9	C infected by someone not already infected
2020-03-31 22:47:59.623535	u/Dopeydragoon	fm2yig3	u/Oli15768	fm2xtd5	C infected by someone not already infected
2020-04-01 23:21:43.320940	u/joeymonster88	fm6m9qv	u/theMeatman7	fm6irx6	C infected by someone not already infected
2020-04-02 03:02:25.093966	u/Donald_buggar	fm72g4b	u/theMeatman7	fm6vlm8	C infected by someone not already infected
2020-04-02 03:28:20.583997	u/Bubble-Guppie	fm73y24	u/Bit_of_a_Hater	fm72wa0	C infected by someone not already infected
2020-04-02 06:22:28.257783	u/loloider123	fm7dkua	u/Bit_of_a_Hater	fm72wa0	C infected by someone not already infected
2020-04-02 13:28:59.302711	u/Ben_dover56	fm8feim	u/UnKnOwNLIKER	fm7vjwi	C infected by someone not already infected
2020-04-02 16:19:42.120531	u/a-random-pan-enby	fm8z561	u/Durmath	fm8ywra	C infected by someone not already infected
2020-04-02 22:22:43.873716	u/Jamstroxian	fm9zzwc	u/Durmath	fm91z9f	C infected by someone not already infected
2020-04-03 03:21:16.315794	u/awesomenessest	fmalmri	u/my-name-is-blank	fmakz7z	C infected by someone not already infected
2020-04-03 03:21:26.568935	u/MrChakalski	fmaln0c	u/my-name-is-blank	fmakz7z	C infected by someone not already infected
2020-04-03 03:32:20.710100	u/kockamester88	fmam8cn	u/my-name-is-blank	fmakz7z	C infected by someone not already infected
2020-04-03 03:39:05.732678	u/Brxken_Fire	fmamm5s	u/GloryToDucks39	fmaerht	C infected by someone not already infected
2020-04-04 07:09:25.210948	u/Vengeance1020	fmebsql	u/NotFunnyBuddy	fmeaxl4	C infected by someone not already infected
2020-04-05 21:22:31.915935	u/Kerimio	fmjpxyz	u/Oli15768	fmjpu7n	C infected by someone not already infected
2020-04-06 03:46:39.541500	u/Champ9889	fmklh91	u/my-name-is-blank	fmklesp	C infected by someone not already infected
2020-04-10 13:57:02.772222	u/Barkerin0	fn0fh5c	u/theMeatman7	fmeb0j2	C infected by someone not already infected
2020-04-11 02:48:11.724676	u/Nuttsuccer69	fn2fwxj	u/5amukai	fn1avyb	C infected by someone not already infected
2020-04-11 05:29:24.484809	u/Takees	fn2os9z	u/NotFunnyBuddy	fn2oocy	C infected by someone not already infected
2020-04-12 21:46:27.691692	u/hareltestbed	fn8i88e	u/5amukai	fn8gg0f	C infected by someone not already infected
2020-04-13 10:17:01.398261	u/JoergenV	fn9y9tk	u/TheCanadianm8	fn9x0yu	C infected by someone not already infected
2020-04-14 10:46:57.507375	u/RedNoodleHouse	fndqglf	u/5amukai	fnd93ku	C infected by someone not already infected
2020-04-15 06:42:12.376132	u/Rafael3DS	fngvyn8	u/my-name-is-blank	fngu0wj	C infected by someone not already infected
2020-04-15 17:36:27.860374	u/The_Memester_42069	fnitmwr	u/TheEgyptDog	g1uwlq	S infected by someone not already infected
2020-04-17 14:39:42.499611	u/Dukester8904	fnpmmwc	u/5amukai	fnotkxd	C infected by someone not already infected"""

comments = open("../total_comments.log", "r")
infections = open("../total_infections.dedupe3.log", "r")

with open('../../../src/creds.json', 'r') as fp:
    credentials = json.load(fp)

_reddit = praw.Reddit(
    client_id=credentials["CLIENT_ID"],
    client_secret=credentials["CLIENT_SECRET"],
    user_agent=credentials["CLIENT_AGENT"],
    username=credentials["CLIENT_USERNAME"],
    password=credentials["CLIENT_PASSWORD"]
)

look_at = dict()
after = "2020-03-20 19:59:59"
pretbf = set()
to_be_fixed = to_be_fixed.split("\n")
final_to_be_fixed = []
for tbf in to_be_fixed:
    tbf = tbf.strip().split("\t")
    if tbf[3] not in pretbf:
        print("Gathering", tbf)
        final_to_be_fixed.append(tbf)
    pretbf.add(tbf[3])

input()


def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.datetime.fromtimestamp (epoch) - datetime.datetime.utcfromtimestamp (epoch)
    return utc + offset


for tbf in final_to_be_fixed:
    print(tbf)
    tbf = [tbf[0], tbf[3]]

    user = tbf[1][2:]
    before = tbf[0].split(".")[0]
    look_at[tbf[1]] = []
    for cmt in _reddit.redditor(user).comments.new(limit=None):
        if str(utc2local(datetime.datetime.utcfromtimestamp(cmt.created_utc))) < after:
            break
        if cmt.subreddit != "memes":
            continue
        parent = cmt.parent()
        look_at[tbf[1]].append([str(utc2local(datetime.datetime.utcfromtimestamp(cmt.created_utc))), str(cmt.id), str(parent.author.name) if hasattr(parent.author, "name") else "u/deleted", "C" if type(parent) == models.Comment else "S", str(parent.id)])
        print(look_at[tbf[1]][-1], "https://www.reddit.com" + cmt.permalink)

with open("../manual_fixes.json", "w") as fp:
    json.dump(look_at, fp)
