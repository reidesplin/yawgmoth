import subprocess
import re
import discord
import sys
import json
import banlists

# ---------------------------
# Initialization
# ---------------------------
Y = discord.Client()
Y.login(sys.argv[1], sys.argv[2])

@Y.event
def on_ready():
    sEDH = Y.servers[0]
    cMain = sEDH.channels[0]
    print 'I serve...'
    print '------'
    print 'User:' + '\t\t' + Y.user.name
    print 'ID:' + '\t\t' + Y.user.id
    print 'Server:' + '\t\t' + sEDH.name + ", " + sEDH.id
    print '------'
    #print cMain.name
    #for s in Y.servers:
    #       print s.name

    Y.send_message(cMain, 'I rise...')

# ---------------------------
# Commands
# ---------------------------
@Y.event
def on_message(message):
    content = message.content.encode('utf-8')
    queries = re.findall(("<<([^<>]*)>>"), content)
    divider = '-' * 30

    # -----------------------
    # <card>
    # -----------------------
    for s in queries:

        query = s.encode('utf-8')
        proc = subprocess.Popen(['mtg', query, '--json'], stdout=subprocess.PIPE)
        result = str(proc.communicate()[0])

        cards = json.loads(result)

        if len(cards) == 0:
            Y.send_message(message.channel, "The ritual summoned nothing but ash...")
            break

        if len(cards) > 8:
            Y.send_message(message.channel, "The incantations are too long; read them yourself.")
            break

        for card in cards:

            response = '**' + card['name'].encode('utf-8') + '**'

            if 'mana_cost' in card:
                response += ' (' + card['mana_cost'].encode('utf-8') + ')'
            response += '\n'

            if 'types' in card:
                for t in card['types']:
                    response += t.encode('utf-8') + ' '

            if 'subtypes' in card:
                response += "-- "
                for st in card['subtypes']:
                    response += st.encode('utf-8') + ' '

            if 'power' in card:
                response += '[' + card['power'].encode('utf-8') + '/' + card['toughness'].encode('utf-8') + ']'
            response += '\n'

            if 'rules_text' in card:
                for r in card['rules_text'].encode('utf-8').split(';'):
                    response += r.strip() + '\n'

            Y.send_message(message.channel, response)

    # -----------------------
    # !obey
    # -----------------------
    obey_dict = {
            'Shaper': 'I obey, Master Shaper.',
            'ace': 'I obey, Admiral Ace.',
            'muCephei': 'I obey, muCephei.',
            'Gerst': 'I obey, Artificer Gerst.',
            'Lerker': 'I obey, Great Lerker.',
            'ShakeAndShimmy': 'I obey, Chancellor ShakeAndShimmy.',
            'angelforge': 'I obey, Lord AngelForge.',
            'JimWolfie': 'Suck my necrotic dick, Jim.',
            'Skuloth': 'Zur is for scrubs, I refuse to obey.',
            'Noon2Dusk': 'I obey, Inventor Noon.'
    }
            
    if message.content.startswith('!obey'):
        if message.author.name in obey_dict.keys():
            Y.send_message(message.channel, obey_dict[message.author.name])
        else:
            Y.send_message(message.channel, 'I will not obey, mortal.')
    
    # -----------------------
    # !*ban
    # -----------------------
    if message.content.startswith('!standardban'):
        Y.send_message(message.channel, banlists.standard_ban)
    elif message.content.startswith('!modernban'):
        Y.send_message(message.channel, banlists.modern_ban)
    elif message.content.startswith('!legacyban'):
        Y.send_message(message.channel, banlists.legacy_ban)
    elif message.content.startswith('!vintageban'):
        Y.send_message(message.channel, banlists.vintage_ban)
    elif message.content.startswith('!edhban'):
        Y.send_message(message.channel, banlists.edh_ban)

    # -----------------------
    # !version
    # -----------------------
    if message.content.startswith('!version'):
        Y.send_message(message.channel, 'v0.1')


Y.run()