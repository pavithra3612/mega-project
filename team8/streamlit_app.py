import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#st.title("HPSA Score Comparison")
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1; 
               font-family: Helvetica; font-size: 50px;'>
        HPSA Score Comparison
    </h1>
    """,
    unsafe_allow_html=True
)

#Main New Mexico Data
NMdata = pd.read_csv("FinalProjectDataPt2.csv")

#print(NMdata.columns.tolist())

#Convert string to numbers
NMdata["HPSA Score"] = pd.to_numeric(NMdata["HPSA Score"], errors="coerce")

#Drop missing values
clean_score_col = NMdata["HPSA Score"].dropna()

#Main California Data
#cali = pd.read_csv("CaliDataFinal.csv")

caliData = pd.read_csv("CaliDataFinal.csv", encoding="latin1")


#Converting if it doesnt work
caliData["HPSA Score"] = pd.to_numeric(caliData["HPSA Score"], errors="coerce")

cali_clean = caliData["HPSA Score"].dropna()

#Main Massachusetts Data
massData = pd.read_csv("MassachusettsData.csv", encoding="latin1")

#Convert Var8
massData["Unnamed: 7"] = pd.to_numeric(massData["Unnamed: 7"], errors="coerce")

mass_clean = massData["Unnamed: 7"].dropna()

#Plotting
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

fig.subplots_adjust(hspace=1.0)

#HPSA New Mexico plotting
axs[0].bar(range(len(clean_score_col)), clean_score_col, color="red")
axs[0].set_title("HPSA Score Within New Mexico")
axs[0].set_xlabel("Different Disciplines in NM")
axs[0].set_ylabel("HPSA Scores")

axs[0].annotate(
    f"Average HPSA Score for New Mexico: {clean_score_col.mean():.2f}",
    xy=(0.5, 0), xycoords="axes fraction",
    xytext=(0, -40), textcoords="offset points",
    ha="center", va="top"
)

#HPSA California plotting
axs[1].bar(range(len(cali_clean)), cali_clean, color="blue")
axs[1].set_title("HPSA Score Within California")
axs[1].set_xlabel("Different Disciplines in California")
axs[1].set_ylabel("HPSA Scores")

axs[1].annotate(
    f"Average HPSA Score for California: {cali_clean.mean():.2f}",
    xy=(0.5, 0), xycoords="axes fraction",
    xytext=(0, -40), textcoords="offset points",
    ha="center", va="top"
)

#HPSA Massachusetts plotting
axs[2].bar(range(len(mass_clean)), mass_clean, color="green")
axs[2].set_title("HPSA Score Within Massachusetts")
axs[2].set_xlabel("Different Disciplines in Massachusetts")
axs[2].set_ylabel("HPSA Scores")

axs[2].annotate(
    f"Average HPSA Score for Massachusetts: {mass_clean.mean():.2f}",
    xy=(0.5, 0), xycoords="axes fraction",
    xytext=(0, -40), textcoords="offset points",
    ha="center", va="top"
)

plt.tight_layout()
#plt.show()

#Sending Plot to Streamlit
st.pyplot(fig)
