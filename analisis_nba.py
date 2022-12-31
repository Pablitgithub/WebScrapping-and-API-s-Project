import requests
from fpdf import FPDF
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def extract():
    headers = {'Ocp-Apim-Subscription-Key': 'b4835e6af3494b71ac8602abca02cf1c'}
    api = requests.get(
        'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/2022', headers=headers)
    data = api.json()
    return data


def transform(data):

    df = pd.DataFrame(data)
    df_brk = df[df['Name'] == 'Brooklyn Nets']

    # Eliminamos las columnas que no nos interesan
    del(df_brk['LineupStatus'])
    del(df_brk['OpponentStat'])
    del(df_brk['IsClosed'])
    del(df_brk['GlobalTeamID'])
    del(df_brk['Updated'])
    del(df_brk['StatID'])
    del(df_brk['TeamID'])
    del(df_brk['Season'])
    del(df_brk['FantasyPointsDraftKings'])
    del(df_brk['FantasyPointsFanDuel'])
    del(df_brk['FantasyPointsYahoo'])
    del(df_brk['LineupConfirmed'])
    del(df_brk['FantasyPointsFantasyDraft'])
    del(df_brk['FantasyPoints'])
    del(df_brk['PlayerEfficiencyRating'])
    del(df_brk['AssistsPercentage'])
    del(df_brk['StealsPercentage'])
    del(df_brk['BlocksPercentage'])
    del(df_brk['TurnOversPercentage'])
    del(df_brk['UsageRatePercentage'])
    del(df_brk['OpponentPosition'])
    del(df_brk['OffensiveReboundsPercentage'])
    del(df_brk['DefensiveReboundsPercentage'])
    del(df_brk['TotalReboundsPercentage'])
    del(df_brk['SeasonType'])
    return df_brk, df


def load(df, df_brk):

    #####Bar chart#####
    df = df.sort_values(by='Points', ascending=False)
    fig1 = plt.figure(figsize=(10, 10))
    barlist = plt.bar(df['Name'], df['Points'],)
    barlist[8].set_color('r')
    plt.title('Points per team')
    plt.xlabel('Team')
    plt.ylabel('Points')
    plt.xticks(rotation=90)
    fig1.savefig('teamspoints.jpg', bbox_inches='tight')

#####Pie chart#####
    w = df_brk['Wins'].sum()
    l = df_brk['Losses'].sum()
    labels = ['Wins', 'Losses']
    sizes = [w, l]
    colors = sns.color_palette('pastel')[0:2]
    fig2 = plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title('Wins and losses')
    plt.legend()
    plt.savefig('winslosses.jpg', bbox_inches='tight')

#####Bar chart shooting#####
    shooting = ['Two Pointers', 'Three Pointers', 'Free Throws']
    attempted = [df_brk['TwoPointersAttempted'].sum(
    ), df_brk['ThreePointersAttempted'].sum(), df_brk['FreeThrowsAttempted'].sum()]
    made = [df_brk['TwoPointersMade'].sum(), df_brk['ThreePointersMade'].sum(),
            df_brk['FreeThrowsMade'].sum()]
    x = np.arange(len(shooting))
    width = 0.35
    fig3, ax = plt.subplots(figsize=(10, 10))
    attempteds = ax.bar(x-width/2, attempted, width, label='Attempted')
    mades = ax.bar(x+width/2, made, width, label='Made')
    ax.set_ylabel('Shots')
    ax.set_title('Shooting')
    ax.set_xticks(x, shooting)
    ax.legend()
    ax.bar_label(attempteds, padding=3)
    ax.bar_label(mades, padding=3)
    fig3.tight_layout()
    plt.savefig('shooting.jpg', bbox_inches='tight')


#####Tabla#####

    df_tabla = df_brk.transpose()
    # rename both columns
    df_tabla.reset_index(inplace=True)
    df_tabla.columns = ['Stat', 'Value']
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(48, 2, 1, frameon=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    pd.plotting.table(ax, data=df_tabla, loc='center')
    plt.savefig('team_stats_table.jpg', bbox_inches='tight')

    pdf = FPDF()

    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w=0, h=20, ln=1, txt='NBA ANALYSIS (Brooklyn Nets) ', align='C')
    pdf.image('nets_logo.png', x=75, y=pdf.get_y()+10, w=50, h=50)
    pdf.image('nets_team.jpg', x=10, y=pdf.get_y()+70, w=190, h=100)

    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w=0, h=20, ln=1, txt='Overall Brooklyn Nets Statistics ', align='C')
    pdf.image('team_stats_table.jpg', x=10, y=pdf.get_y()+20, w=190, h=220)

    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(
        w=0, h=5, txt='Points compared with other teams.', align="C")
    pdf.image('teamspoints.jpg', x=10, y=pdf.get_y()+20, w=190, h=190)
    pdf.set_font("Arial", size=14)
    pdf.set_y(pdf.get_y()+225)
    pdf.multi_cell(
        w=0, h=5, txt='As we can see the Brooklyn Nets are in the top 10s of the teams with the most points.', align="C")

    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(
        w=0, h=5, txt='Brooklyn Nets wins and losses .', align="C")
    pdf.image('winslosses.jpg', x=10, y=pdf.get_y()+20, w=190, h=190)
    pdf.set_font("Arial", size=14)
    pdf.set_y(pdf.get_y()+225)
    pdf.multi_cell(
        w=0, h=5, txt='As we can see the Brooklyn Nets have a greater percentage of wins than losses', align="C")

    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(
        w=0, h=5, txt='Shooting stats.', align="C")
    pdf.image('shooting.jpg', x=10, y=pdf.get_y()+20, w=190, h=190)
    # add text under the image
    pdf.set_font("Arial", size=14)
    pdf.set_y(pdf.get_y()+225)
    pdf.multi_cell(
        w=0, h=5, txt='As we can see the free throw shooting has the best percentage, while the two pointer is more attempted obviously and outside the three point line, the Brooklyn Nets miss more than 50% of their shoots.', align="C")

    pdf.output('NBA_analysis.pdf')


if __name__ == '__main__':
    api = extract()
    df_brk, df = transform(api)
    load(df, df_brk)
