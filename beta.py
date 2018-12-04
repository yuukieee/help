import discord
from discord.ext import commands
import time
import datetime
import asyncio
import random
import json
import requests

client = commands.Bot(command_prefix='c!')
COLOUR = 0xff6e00

@client.event
async def on_ready ():
    print ('Bot Online.')
    await client.change_presence(game=discord.Game(name="Em manutenção.", type=1, url='https://www.twitch.tv/theflaamer'),status='streaming')

@client.event
async def on_member_join(member):
    if member.server.id == '483843901095018496':
        welcomemb = discord.Embed(color=0xff6e00, title="Bem-vindo(a) ao nosso servidor! Leia as regras e seja um bom membro.",
                              description="{}".format(member.mention))
        canal = client.get_channel("483847414071951364")  #canal  
        welcomemb.set_image(url="https://cdn.discordapp.com/attachments/509489702257164299/509509889677197333/tumblr_o57qnvomRp1qc5o4jo1_400.gif")
        welcomemb.set_footer(icon_url=member.avatar_url, text=member.name)
        await client.send_message(canal, embed=welcomemb)

@client.event
async def on_member_remove(member):
    if member.server.id == '483843901095018496':
        leavemb = discord.Embed(color=0xff6e00, title="{0} ({0.id}) saiu do servidor 😦 ".format(member))
        leavemb.set_image(url="https://cdn.discordapp.com/attachments/490242962501009428/499267148363989002/giphy.gif")
        canal = client.get_channel("483847414071951364") #canal
        welcomemb.set_footer(icon_url=member.avatar_url, text=member.name)
        await client.send_message(canal, embed=leavemb)

@client.event
async def on_message(message):
    if message.content.lower().startswith("c!sorteio"):
        if message.author.server_permissions.administrator:
            n = random.choice(list(message.server.members))
            n1 = '{}'.format(n.name)
            m1 = discord.utils.get(message.server.members, name="{}".format(n1))
            embed = discord.Embed(
                title="🌌 | Escolhendo um membro...",
                colour=0xff6e00,
                description="🌠 | O membro escolhido foi {}".format(m1.mention)
            )
            hh = await client.send_message(message.channel, "{}".format(m1.mention))
            await client.delete_message(hh)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(
                "❌ | {} você não tem permissão para usar esse comando!".format(message.author.mention))

    if message.content.startswith("c!ban"):
        if not message.author.server_permissions.ban_members:
            return await client.send_message(message.channel,"**❌ | Você não tem permissão para usar esse comando!**")
        try:
            user = message.mentions[0]
            await client.send_message(message.channel,
                                      "**✔️ | O usuario <@{}> foi banido do servidor.**".format(user.id))
            await client.ban(user, delete_message_days=1)
        except IndexError:
            await client.send_message(message.channel, "**🔸 | Você não mencionou alguem para ser banido!**")
        except discord.Forbidden:
            await client.send_message(message.channel,"**❌ | Não foi possivel banir esse usuário... Verifique se eu tenho função ADM e se meu cargo está acima do dele(a).**!")
        finally:
            pass

    if message.content.lower().startswith('c!unban'):
        if not message.author.server_permissions.ban_members:
            return await client.send_message(message.channel, "**❌ | Você não tem permissão para usar esse comando!**")
        try:
            uid = message.content[7:]
            user = await client.get_user_info(uid)
            await client.send_message(message.channel, "**✔️ | O usuário foi desbanido do servidor.**")
            return await client.unban(user)
        except:
            await client.send_message(message.channel, "**❌ | Você não deixou claro um membro!**")
        finally:
            pass

    if message.content.lower().startswith('c!mute'):
        try:
            if not message.author.server_permissions.administrator:
                return await client.send_message(message.channel, '**❌ | Você não tem permissão para usar esse comando!**')
            author = message.author.mention
            user = message.mentions[0]
            motivo = message.content[29:]
            cargo = discord.utils.get(message.author.server.roles,
                                      name='Muted')
            await client.add_roles(user, cargo)
            await client.send_message(message.channel,
                                      '✔️ | Usuário: {} foi mutado pelo moderador: {} pelo motivo: {}.'.format(user.mention, author, motivo))
        except:
            await client.send_message(message.channel, "**❌ | Você não deixou claro um membro!**")

    if message.content.lower().startswith('c!unmute'):
        try:
            if not message.author.server_permissions.administrator:
                return await client.send_message(message.channel, '**❌ | Você precisa da permissão de ADM!**')
            author = message.author.mention
            user = message.mentions[0]
            motivo = message.content[29:]
            cargo = discord.utils.get(message.author.server.roles,
                                      name='Muted')
            await client.remove_roles(user, cargo)
            await client.send_message(message.channel,
                                      '✔️ | O Usuário: {} foi desmutado pelo Administrador: {} pelo motivo: {}.'.format(
                                          user.mention, author, motivo))
        except:
            await client.send_message(message.channel, "**❌ | Você deve especificar um usuario!**.")

    if message.content.lower().startswith('c!userinfo'):
        try:
            user = message.mentions[0]
            server = message.server
            embedinfo = discord.Embed(title='💖 | Informações do usuário:', color=0xff6e00, )
            embedinfo.set_thumbnail(url=user.avatar_url)
            embedinfo.add_field(name='Nome:', value=user.name)
            embedinfo.add_field(name='Apelido', value=user.nick)
            embedinfo.add_field(name='ID:', value=user.id)
            embedinfo.add_field(name='Entrou em:', value=user.joined_at.strftime("%d %b %Y as %H:%M"))
            embedinfo.add_field(name='Server criado em:', value=server.created_at.strftime("%d %b %Y %H:%M"))
            embedinfo.add_field(name='Jogando:', value=user.game)
            embedinfo.add_field(name="Status:", value=user.status)
            embedinfo.add_field(name='Cargos:', value=([role.name for role in user.roles if role.name != "@everyone"]))
            await client.send_message(message.channel, embed=embedinfo)
        except ImportError:
            await client.send_message(message.channel, '❌ | Ocorreu um erro. Por favor, reporte ao <@442702816595804190>.')
        except:
            await client.send_message(message.channel, '❌ | Mencione um usuário válido')
        finally:
            pass

    if message.content.lower().startswith('c!news'):
        reqnews = requests.get(
            'https://newsapi.org/v2/top-headlines?sources=globo&apiKey=6888a62938c744a79d4dec22809ba3d1')
        lernews = json.loads(reqnews.text)
        authornews = (str(lernews['articles'][0]['author']))
        titulonews = (str(lernews['articles'][0]['title']))
        descriptionnews = (str(lernews['articles'][0]['description']))
        urlnews = (str(lernews['articles'][0]['url']))
        datanews = (str(lernews['articles'][0]['publishedAt']))
        imgnews = (str(lernews['articles'][0]['urlToImage']))
        embednews = discord.Embed(color=0xff6e00)
        embednews.add_field(name='Autor Da notícia:', value="{}".format(authornews))
        embednews.add_field(name='Título:', value="{}".format(titulonews))
        embednews.add_field(name='Descrição:', value="{}".format(descriptionnews))
        embednews.add_field(name='Link da noticia:', value="{}".format(urlnews))
        embednews.set_footer(text='Data da noticia: ' + datanews)
        embednews.set_thumbnail(url=imgnews)
        await client.send_message(message.channel, embed=embednews)

    prefixo = "c!"
    if message.content.startswith(prefixo + "avatar"):
        xtx = message.content.split(' ')
        if len(xtx) == 1:
            useravatar = message.author
            avatar = discord.Embed(
                title="📸 | Esse avatar pertence ao membro: {}".format(useravatar.name),
                color=0xff6e00,
                description="🖱 | [Clique aqui](" + useravatar.avatar_url + ") para fazer download da imagem."
            )

            avatar.set_image(url=useravatar.avatar_url)
            avatar.set_footer(text="⌨️ | Comando usado por: {}#{}".format(useravatar.name, useravatar.discriminator))
            await client.send_message(message.channel, embed=avatar)
        else:
            try:
                useravatar = message.mentions[0]
                avatar = discord.Embed(
                    title="📸 | Esse avatar pertence ao membro: {}".format(useravatar.name),
                    color=0xff6e00,
                    description="🖱 | [Clique aqui](" + useravatar.avatar_url + ") para fazer download da imagem."
                )

                avatar.set_image(url=useravatar.avatar_url)
                avatar.set_footer(text="⌨️ | Comando usado por: {}".format(message.author))
                await client.send_message(message.channel, embed=avatar)

            except IndexError:
                a = len(prefixo) + 7
                uid = message.content[a:]
                useravatar = message.server.get_member(uid)
                avatar = discord.Embed(
                    title="📸 | Esse avatar pertence ao membro: {}".format(useravatar.name),
                    color=0xff6e00,
                    description="🖱 | [Clique aqui](" + useravatar.avatar_url + ") para fazer download da imagem."
                )

                avatar.set_image(url=useravatar.avatar_url)
                avatar.set_footer(text="⌨️ | Comando usado por: {}".format(message.author))
                await client.send_message(message.channel, embed=avatar)

    if message.content.startswith('c!denunciar'):
        await client.send_message(message.author,
                                  '**🔰 | Qual usuário você deseja denunciar? {}**'.format(message.author.mention))
        jogador = await client.wait_for_message(author=message.author)
        await client.send_message(message.author, '**🔰 | Qual o motivo da denuncia? {}**'.format(message.author.mention))
        motivo = await client.wait_for_message(author=message.author)
        await client.send_message(message.author, '**🔰 | Que dia aconteceu isso? {}**'.format(message.author.mention))
        dia = await client.wait_for_message(author=message.author)
        await  client.send_message(message.author, '**🔰 | Por favor, envie alguma prova {}, se for mandar imagem, mande em link por favor.**'.format(message.author.mention))
        prova = await client.wait_for_message(author=message.author)
        canal = client.get_channel('488141362928156714')
        embed = discord.Embed(colour=0xff6e00,
                              description="❕ | O usuário: {} acabou de denunciar!".format(message.author.mention))
        embed.add_field(name='Motivo:', value=motivo.content)
        embed.add_field(name='Data do ocorrido:', value=dia.content)
        embed.add_field(name='Prova:', value=prova.content)
        embed.add_field(name='Usuário denunciado:', value=jogador.content)
        await client.send_message(canal, embed=embed)

    if message.content.lower().startswith('c!nick'):
        if not message.author.server_permissions.administrator:
            await client.send_message(message.channel, 'Você não tem permissão para isso..')
        try:
            user = message.mentions[0]
            msg = str(message.content[12:]).replace('<', '').replace('>', '').replace('@', '').replace(user.id, '')
            await client.change_nickname(user, msg)
            await client.send_message(message.channel, 'Apelido mudado :D')
        except:
            await client.send_message(message.channel, 'Diga um usuário..')

    if message.content.startswith("c!kick"):
        if not message.author.server_permissions.kick_members:
            return await client.send_message(message.channel,
                                             "**❌ | Você não tem permissão para executar esse comando!**")
        try:
            user = message.mentions[0]
            await client.send_message(message.channel,
                                      "**✔️ | O usuario(a) <@{}> foi kickado com sucesso do servidor.**".format(user.id))
            await client.kick(user)
        except:
            await client.send_message(message.channel, "**❌ | Você deve especificar um usuario para kickar!**")

    if message.content.lower().startswith('c!say'):
        if message.author.server_permissions.administrator:
           try:
              msg = str(message.content).replace("y!say", "")
              embed = discord.Embed(description=msg, color=0xff6e00)
              await client.send_message(message.channel, embed=embed)
              await client.delete_message(message)
           except:
              await  client.send_message(message.channel, "❌ | Digite algo!")
        else:
           await client.send_message(message.channel, "❌ | Sem permissão!")

    if message.content.lower().startswith('c!8ball'):
        try:
            respostas = ['Sim','Não','Talvez','Nunca','Claro']
            resposta = random.choice(respostas)
            mensagem = message.content[7:]
            embed = discord.Embed(color=0xff6e00)
            embed.add_field(name="Pergunta:", value='{}'.format(mensagem),inline=False)
            embed.add_field(name="Resposta:", value=resposta,inline=False)
            await client.send_message(message.channel, embed=embed)
            await client.delete_message(message)
        except:
            await client.send_message(message.channel, '❌ | Você precisa perguntar alguma coisa!')

    if message.content.startswith('c!serverinfo'):
        
        user = message.author.name
        
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        
        serverinfo_embed = discord.Embed(title="\n", description="🛤 | Segue abaixo as informações desse servidor <3", color=0xff6e00)
        serverinfo_embed.set_thumbnail(url=message.server.icon_url)
        serverinfo_embed.set_footer(text="{} ⌚️ {}".format(user, horario))
        serverinfo_embed.add_field(name="Nome:", value=message.server.name, inline=True)
        serverinfo_embed.add_field(name="Dono:", value=message.server.owner.mention)
        serverinfo_embed.add_field(name="ID:", value=message.server.id, inline=True)
        serverinfo_embed.add_field(name="Cargos:", value=len(message.server.roles), inline=True)
        serverinfo_embed.add_field(name="Canais de texto:", value=len([message.channel.mention for channel in message.server.channels if channel.type==discord.ChannelType.text]), inline=True)
        serverinfo_embed.add_field(name="Canais de voz:", value=len([message.channel.mention for channel in message.server.channels if channel.type==discord.ChannelType.voice]), inline=True)
        serverinfo_embed.add_field(name="Membros:", value=len(message.server.members), inline=True)
        serverinfo_embed.add_field(name="Bots:", value=len([user.mention for user in message.server.members if user.bot]), inline=True)        
        serverinfo_embed.add_field(name="Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"), inline=True)
        serverinfo_embed.add_field(name="Região:", value=str(message.server.region).title(), inline=True)
        await client.send_message(message.channel,embed=serverinfo_embed)


    if message.content.startswith("c!servidores"):
            servidores = '\n'.join([s.name for s in client.servers])
            embe = discord.Embed(title="⚙️ | Estou online em " + str(len(client.servers)) + " servidores com " + str(len(set(client.get_all_members()))) + " membros!",
                                color=0xff6e00,
                                description=servidores)
            await client.send_message(message.channel, embed=embe)

    elif message.content.lower().startswith("c!busca"):

        await client.delete_message(message)

        words = 'https://www.google.com/search?q=' + message.content[8:].strip().replace(' ', '+')

        await client.send_message(message.channel, words)

    if message.content.startswith(client.user.mention):
        await client.send_message(message.channel, "Olá 😄, sou um pequeno bot desenvolvido pelo <@442702816595804190> exclusivamente para o servidor ***Viciados em Cahfé***, se quiser saber meus comandos, abra o link https://github.com/Awesome211/HelpALCM. Obrigado por me usar 😏")

    if message.content.lower().startswith('c!info'):
        await client.delete_message(message)
        embedbot = discord.Embed(
            title='**🤖 ! Informações do Bot**',
            color=0xff6e00,
            description='\n'
        )
        embedbot.set_thumbnail(url="https://cdn.discordapp.com/attachments/509489702257164299/509508637861871626/76e898548dcae7e6caae75eeadd3b8f1.png")
        embedbot.add_field(name='`💮 | Nome`', value=client.user.name, inline=True)
        embedbot.add_field(name='`◼ | Id do bot`', value=client.user.id, inline=True)
        embedbot.add_field(name='💠 | Criado em', value=client.user.created_at.strftime("%d %b %Y %H:%M"))
        embedbot.add_field(name='📛 | Tag', value=client.user)
        embedbot.add_field(name='‍💻 | Servidores', value=len(client.servers))
        embedbot.add_field(name='👥 | Usuarios', value=len(list(client.get_all_members())))
        embedbot.add_field(name='‍⚙️ | Programador', value="`Awesome`") #Aqui você coloca seu nome/discord
        embedbot.add_field(name='🐍 Python  | Versão', value="`3.6.6`") #Aqui você coloca a versão do python que você está utilizando!
        embedbot.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)

        await client.send_message(message.channel, embed=embedbot)

    if message.content.startswith("c!timer"):
        mensagem = "**5**"
        await client.send_message(message.channel, mensagem)
        await asyncio.sleep(1)
        mensagem = "**4**"
        await client.send_message(message.channel, mensagem)
        await asyncio.sleep(1)
        mensagem = "**3**"
        await client.send_message(message.channel, mensagem)
        await asyncio.sleep(1)
        mensagem = "**2**"
        await client.send_message(message.channel, mensagem)
        await asyncio.sleep(1)
        mensagem = "**1**"
        await client.send_message(message.channel, mensagem)

    if message.content.lower().startswith('c!hug'):
        try:
            hugimg = ['http://media1.tenor.com/images/e58eb2794ff1a12315665c28d5bc3f5e/tenor.gif?itemid=10195705',
                      'http://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif?itemid=4900166',
                      'http://media1.tenor.com/images/11889c4c994c0634cfcedc8adba9dd6c/tenor.gif?itemid=5634578',
                      'http://media1.tenor.com/images/d7529f6003b20f3b21f1c992dffb8617/tenor.gif?itemid=4782499',
                      'https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935',
                      'https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788',
                      'https://media1.tenor.com/images/3c83525781dc1732171d414077114bc8/tenor.gif?itemid=7830142']
            hug = random.choice(hugimg)
            hugemb = discord.Embed(title='Abraço :heart:',
                                   description='**{}** Ele(a) recebeu um abraço de **{}**! Casal Fofo! :heart_eyes: '
                                   .format(message.mentions[0].name, message.author.name), color=0xff6e00)
            hugemb.set_image(
                url=hug)
            hugemb.set_footer(text="Direitos do código para: iColdZ")
            await client.send_message(message.channel, embed=hugemb)
        except IndexError:
            await client.send_message(message.channel, 'Você precisa mencionar um usuário específico para abraçar!')

    if message.content.lower().startswith('c!kiss'):
        try:
            hugimg = ['https://cdn.discordapp.com/attachments/493872493753401345/499271073473495045/tenor_5.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499271075268657152/tenor_6.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499271056951869471/tenor_1.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499271043450535953/tenor_2.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499271041873608704/tenor_3.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499271013712920576/tenor_4.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499270865981145099/tenor.gif']
            hug = random.choice(hugimg)
            hugemb = discord.Embed(title='Beijinho :heart:',
                                   description='**{}** recebeu um beijo de **{}**! Que fofo! :heart_eyes: '
                                   .format(message.mentions[0].name, message.author.name), color=0xff6e00)
            hugemb.set_image(
                url=hug)
            hugemb.set_footer(text="Direitos do código para: iColdZ")
            await client.send_message(message.channel, embed=hugemb)
        except IndexError:
            await client.send_message(message.channel, 'Você precisa mencionar um usuário específico para beijar!')

    if message.content.lower().startswith('c!slap'):
        try:
            hugimg = ['https://cdn.discordapp.com/attachments/493872493753401345/499274286159101972/giphy.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274278865338388/giphy_2.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274203053293578/giphy_5.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274196036354058/giphy_1.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274171721711646/giphy_6.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274169876217867/giphy_4.gif',
                      'https://cdn.discordapp.com/attachments/493872493753401345/499274082852929546/giphy_3.gif']
            hug = random.choice(hugimg)
            hugemb = discord.Embed(title='Tapa ✋🏼',
                                   description='**{}** parece que o **{}** está com raiva de você! Cuidado! 💫'
                                   .format(message.mentions[0].name, message.author.name), color=0xff6e00)
            hugemb.set_image(
                url=hug)
            hugemb.set_footer(text="Direitos do código para: iColdZ")
            await client.send_message(message.channel, embed=hugemb)
        except IndexError:
            await client.send_message(message.channel, 'Você precisa mencionar um usuário específico para bater!')

    if message.content.lower().startswith('c!ping'):
        channel = message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        ping_embed = discord.Embed(title="🏓 Pong!", color=0xff6e00, description='Meu tempo de resposta é `{}ms`!'.format(round((t2 - t1) * 1000)))
        await client.send_message(message.channel, "", embed=ping_embed)

    if message.content.lower().startswith('c!shippar'):
        try:
            nome = message.mentions[0].name
            nome2 = message.mentions[1].name
            nome3 = len(nome2)
            nome4 = nome3 - 4
            nome5 = nome[0:4]
            nome6 = nome2[nome4:nome3]
            nome7 = nome5 + nome6
            pessoa = message.author.name
            porcentagem = random.randint(10, 100)
            voce = message.author.mention            
            shippar = discord.Embed(title='Será que essa "Shippada" vai ser o Futuro?', 
                description='**O(a) {} Shippou {} com {}! \n {} % de chance de ser VERDADE.\n Junção dos nomes: {}** '.format(voce,message.mentions[0].mention,message.mentions[1].mention,porcentagem, nome7), color=COLOUR,
                timestamp=datetime.datetime.utcnow())
            shippar.set_image(url="https://media.giphy.com/media/x28cIQSn19Tbi/giphy.gif")
            shippar.set_author(name=pessoa, icon_url=message.author.avatar_url)
            shippar.set_thumbnail(url='https://i.imgur.com/743dfAe.png')
            shippar.set_footer(text='By: Punisher#2055')
            await client.send_message(message.channel, embed=shippar)
        except IndexError:
            await client.send_message(message.channel, "{} Você não mencionou dois usuarios".format(message.author.mention))

    if message.content.lower().startswith('c!test'):
        await client.send_message(message.author, "Olá Mundo, estou vivo!")                      

client.run("NTEyNjc0MjQxOTUxNDMyNzA0.DugCNQ._cn06Ybo68L_Is5BYzD9mo71Ebo")