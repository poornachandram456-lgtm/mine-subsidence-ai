import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mine Subsidence Monitoring System",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# MOBILE RESPONSIVE CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

@media only screen and (max-width: 768px) {

    .block-container {
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        padding-top: 0.5rem;
    }

    h1 {
        font-size: 1.55rem !important;
    }

    h2 {
        font-size: 1.25rem !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.25rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LIVE DASHBOARD
# =========================================================

@st.fragment(run_every="2s")
def live_dashboard():

    # =====================================================
    # GENERATE LIVE SENSOR DATA
    # =====================================================

    sensors = []

    for i in range(1, 101):

        tilt = random.uniform(0.10, 0.70)
        displacement = random.uniform(1.0, 6.0)
        vibration = random.uniform(0.01, 0.08)

        chance = random.random()

        if chance < 0.05:

            tilt = random.uniform(1.5, 3.0)
            displacement = random.uniform(12.0, 20.0)
            vibration = random.uniform(0.20, 0.40)
            status = "Critical"

        elif chance < 0.15:

            tilt = random.uniform(0.8, 1.5)
            displacement = random.uniform(7.0, 12.0)
            vibration = random.uniform(0.08, 0.20)
            status = "Warning"

        else:

            status = "Normal"

        sensors.append({
            "Sensor": f"S{i}",
            "Tilt": round(tilt, 2),
            "Displacement": round(displacement, 2),
            "Vibration": round(vibration, 2),
            "Status": status
        })

    df = pd.DataFrame(sensors)

    # =====================================================
    # SENSOR STATUS COUNTS
    # =====================================================

    total_sensors = len(df)

    normal_count = (
        df["Status"] == "Normal"
    ).sum()

    warning_count = (
        df["Status"] == "Warning"
    ).sum()

    critical_count = (
        df["Status"] == "Critical"
    ).sum()

    # =====================================================
    # HEADER
    # =====================================================

    st.title(
        "⛏️ AI-Enabled Mine Subsidence Monitoring System"
    )

    st.caption(
        "Real-Time Monitoring • AI Risk Detection • "
        "Prediction • Early Warning"
    )

    st.divider()

    # =====================================================
    # TOP STATUS CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📡 Total Sensors",
            total_sensors
        )

    with col2:
        st.metric(
            "🟢 Normal",
            normal_count
        )

    with col3:
        st.metric(
            "🟡 Warning",
            warning_count
        )

    with col4:
        st.metric(
            "🔴 Critical",
            critical_count
        )

    st.divider()

    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    left, right = st.columns([2.2, 1])

    # =====================================================
    # LEFT SIDE
    # =====================================================

    with left:

        # =================================================
        # MINE MAP
        # =================================================

        st.subheader(
            "🗺️ Live Mine Deformation Risk Map"
        )

        fig = go.Figure()

        # -------------------------------------------------
        # MINE GRID
        # -------------------------------------------------

        for y in range(10):

            fig.add_trace(
                go.Scatter(
                    x=list(range(10)),
                    y=[y] * 10,
                    mode="lines",
                    line=dict(width=1),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        for x in range(10):

            fig.add_trace(
                go.Scatter(
                    x=[x] * 10,
                    y=list(range(10)),
                    mode="lines",
                    line=dict(width=1),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        # -------------------------------------------------
        # SENSOR POSITIONS
        # -------------------------------------------------

        df["SensorNumber"] = (
            df["Sensor"]
            .str.replace("S", "", regex=False)
            .astype(int)
        )

        df["x"] = (
            (df["SensorNumber"] - 1) % 10
        )

        df["y"] = (
            (df["SensorNumber"] - 1) // 10
        )

        # -------------------------------------------------
        # SENSOR MARKERS
        # -------------------------------------------------

        sensor_symbols = {
            "Normal": "circle",
            "Warning": "diamond",
            "Critical": "x"
        }

        sensor_colors = {
            "Normal": "#00c853",
            "Warning": "#ffb000",
            "Critical": "#ff2b2b"
        }

        for status, symbol in sensor_symbols.items():

            selected = df[
                df["Status"] == status
            ]

            if selected.empty:
                continue

            fig.add_trace(
                go.Scatter(
                    x=selected["x"],
                    y=selected["y"],
                    mode="markers+text",

                    marker=dict(
                        size=14,
                        symbol=symbol,
                        color=sensor_colors[status]
                    ),

                    text=selected["Sensor"],
                    textposition="top center",

                    customdata=selected[
                        [
                            "Tilt",
                            "Displacement",
                            "Vibration"
                        ]
                    ],

                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Tilt: %{customdata[0]}°<br>"
                        "Displacement: "
                        "%{customdata[1]} mm<br>"
                        "Vibration: "
                        "%{customdata[2]} g<br>"
                        "Status: "
                        + status +
                        "<extra></extra>"
                    ),

                    name=status
                )
            )

        # -------------------------------------------------
        # MAP DESIGN
        # -------------------------------------------------

        fig.update_layout(

            height=480,

            # IMPORTANT:
            # This stays constant so Plotly does not reset
            # the user's view every refresh.
            uirevision="mine-map-stable",

            transition={
                "duration": 0
            },

            xaxis=dict(
                title="Mine Panel",
                dtick=1,
                showgrid=True,
                zeroline=False
            ),

            yaxis=dict(
                title="Mine Section",
                dtick=1,
                showgrid=True,
                zeroline=False
            ),

            legend=dict(
                title="Risk Level"
            ),

            margin=dict(
                l=30,
                r=30,
                t=20,
                b=30
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            },
            key="mine_map_live"
        )

        st.caption(
            "Each marker represents a virtual monitoring node. "
            "Sensor conditions are generated by the simulation "
            "engine and updated continuously."
        )

        # =================================================
        # 3D UNDERGROUND MINE MODEL
        # =================================================

        st.subheader(
            "⛏️ 3D Underground Mine Digital Model"
        )

        fig3d = go.Figure()

        # -------------------------------------------------
        # MAIN TUNNEL CORRIDORS
        # -------------------------------------------------

        tunnel_y_positions = [1, 3, 5, 7, 9]
        tunnel_x_positions = [1, 3, 5, 7, 9]

        for y in tunnel_y_positions:

            fig3d.add_trace(
                go.Scatter3d(
                    x=list(range(10)),
                    y=[y] * 10,
                    z=[-2] * 10,
                    mode="lines",
                    line=dict(
                        color="#777777",
                        width=12
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        for x in tunnel_x_positions:

            fig3d.add_trace(
                go.Scatter3d(
                    x=[x] * 10,
                    y=list(range(10)),
                    z=[-2] * 10,
                    mode="lines",
                    line=dict(
                        color="#777777",
                        width=12
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        # -------------------------------------------------
        # OUTER BOUNDARY
        # -------------------------------------------------

        boundary_points = [
            (0, 0),
            (9, 0),
            (9, 9),
            (0, 9),
            (0, 0)
        ]

        fig3d.add_trace(
            go.Scatter3d(
                x=[p[0] for p in boundary_points],
                y=[p[1] for p in boundary_points],
                z=[-0.8] * len(boundary_points),
                mode="lines",
                line=dict(
                    color="#555555",
                    width=10
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

        # -------------------------------------------------
        # ROOF
        # -------------------------------------------------

        fig3d.add_trace(
            go.Mesh3d(
                x=[0, 9, 9, 0],
                y=[0, 0, 9, 9],
                z=[-0.4, -0.4, -0.4, -0.4],
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                opacity=0.08,
                color="#666666",
                hoverinfo="skip",
                showlegend=False
            )
        )

        # -------------------------------------------------
        # FLOOR
        # -------------------------------------------------

        fig3d.add_trace(
            go.Mesh3d(
                x=[0, 9, 9, 0],
                y=[0, 0, 9, 9],
                z=[-2.5, -2.5, -2.5, -2.5],
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                opacity=0.10,
                color="#444444",
                hoverinfo="skip",
                showlegend=False
            )
        )

        # -------------------------------------------------
        # SUPPORT PILLARS
        # -------------------------------------------------

        pillar_positions = [
            (1, 1), (3, 1), (5, 1), (7, 1),
            (1, 5), (3, 5), (5, 5), (7, 5),
            (1, 9), (3, 9), (5, 9), (7, 9)
        ]

        for px, py in pillar_positions:

            fig3d.add_trace(
                go.Scatter3d(
                    x=[px, px],
                    y=[py, py],
                    z=[-2.45, -0.55],
                    mode="lines",
                    line=dict(
                        color="#888888",
                        width=8
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        # -------------------------------------------------
        # SENSOR NODE DATA
        # -------------------------------------------------

        x_3d = []
        y_3d = []
        z_3d = []

        sensor_names = []
        tilt_values = []
        displacement_values = []
        vibration_values = []
        status_values = []

        for _, row in df.iterrows():

            sensor_number = int(
                str(row["Sensor"]).replace("S", "")
            )

            x = (sensor_number - 1) % 10
            y = (sensor_number - 1) // 10

            z = -1.65

            x_3d.append(x)
            y_3d.append(y)
            z_3d.append(z)

            sensor_names.append(row["Sensor"])
            tilt_values.append(row["Tilt"])
            displacement_values.append(
                row["Displacement"]
            )
            vibration_values.append(
                row["Vibration"]
            )
            status_values.append(
                row["Status"]
            )

        # -------------------------------------------------
        # RISK COLOURS
        # -------------------------------------------------

        marker_colors = []

        for status in status_values:

            if status == "Critical":

                marker_colors.append(
                    "#ff2b2b"
                )

            elif status == "Warning":

                marker_colors.append(
                    "#ffb000"
                )

            else:

                marker_colors.append(
                    "#00c853"
                )

        # -------------------------------------------------
        # 3D SENSOR NODES
        # -------------------------------------------------

        fig3d.add_trace(
            go.Scatter3d(

                x=x_3d,
                y=y_3d,
                z=z_3d,

                mode="markers+text",

                text=sensor_names,
                textposition="top center",

                marker=dict(
                    size=6,
                    color=marker_colors,
                    opacity=1.0,
                    line=dict(
                        color="white",
                        width=1
                    )
                ),

                customdata=list(
                    zip(
                        tilt_values,
                        displacement_values,
                        vibration_values,
                        status_values
                    )
                ),

                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Tilt: %{customdata[0]:.2f}°<br>"
                    "Displacement: "
                    "%{customdata[1]:.2f} mm<br>"
                    "Vibration: "
                    "%{customdata[2]:.2f} g<br>"
                    "Risk: %{customdata[3]}"
                    "<extra></extra>"
                ),

                name="Sensor Nodes"
            )
        )

        # -------------------------------------------------
        # 3D LEGEND
        # -------------------------------------------------

        for label, colour in [
            ("Normal", "#00c853"),
            ("Warning", "#ffb000"),
            ("Critical", "#ff2b2b")
        ]:

            fig3d.add_trace(
                go.Scatter3d(
                    x=[None],
                    y=[None],
                    z=[None],
                    mode="markers",
                    marker=dict(
                        size=8,
                        color=colour
                    ),
                    name=label,
                    hoverinfo="skip"
                )
            )

        # -------------------------------------------------
        # 3D LAYOUT
        # -------------------------------------------------

        fig3d.update_layout(

            height=560,

            # IMPORTANT:
            # Stable uirevision prevents the camera from
            # jumping back every 2 seconds.
            uirevision="underground-model-stable",

            transition={
                "duration": 0
            },

            margin=dict(
                l=0,
                r=0,
                t=10,
                b=0
            ),

            legend=dict(
                title="Sensor Risk"
            ),

            scene=dict(

                xaxis=dict(
                    title="Mine X Position",
                    range=[-0.5, 9.5],
                    showgrid=False,
                    zeroline=False
                ),

                yaxis=dict(
                    title="Mine Y Position",
                    range=[-0.5, 9.5],
                    showgrid=False,
                    zeroline=False
                ),

                zaxis=dict(
                    title="Underground Depth",
                    range=[-3, 0],
                    showgrid=True,
                    zeroline=False
                ),

                # Initial camera only.
                # uirevision preserves the user's position
                # after they rotate/zoom.
                camera=dict(
                    eye=dict(
                        x=1.55,
                        y=1.55,
                        z=1.15
                    )
                ),

                aspectmode="manual",

                aspectratio=dict(
                    x=1.3,
                    y=1.3,
                    z=0.55
                )
            )
        )

        st.plotly_chart(
            fig3d,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            },
            key="underground_3d_live"
        )

        st.caption(
            "Interactive 3D digital model of the underground mine. "
            "Sensor nodes change colour according to simulated "
            "risk level. Drag to rotate • Scroll to zoom • "
            "Hover over a sensor for readings."
        )

        st.divider()

    # =====================================================
    # RIGHT SIDE — EARLY WARNING
    # =====================================================

    with right:

        st.subheader("🚨 Early Warning")

        if critical_count > 0:

            st.error(
                f"⚠️ {critical_count} critical "
                f"sensor(s) detected!"
            )

            st.metric(
                "Current Risk",
                "HIGH"
            )

            st.write("### Detected Changes")

            st.write(
                "📐 Abnormal tilt detected"
            )

            st.write(
                "↔️ Increased ground displacement"
            )

            st.write(
                "📳 Abnormal vibration"
            )

            st.write(
                "⚠️ Multiple nearby sensors affected"
            )

            st.write("### Recommended Action")

            st.warning(
                "Inspect the affected mine zone "
                "and initiate appropriate safety "
                "procedures."
            )

        elif warning_count > 0:

            st.warning(
                f"⚠️ {warning_count} sensor(s) "
                f"showing warning conditions."
            )

            st.metric(
                "Current Risk",
                "MEDIUM"
            )

            st.write(
                "Deformation abnormalities are "
                "developing in a localized region."
            )

        else:

            st.success(
                "All sensors currently operating normally."
            )

            st.metric(
                "Current Risk",
                "LOW"
            )

    st.divider()

    # =====================================================
    # LIVE SENSOR MEASUREMENTS
    # =====================================================

    st.subheader(
        "📊 Live Sensor Measurements"
    )

    sensor_col1, sensor_col2, sensor_col3, sensor_col4 = (
        st.columns(4)
    )

    with sensor_col1:

        st.metric(
            "Average Tilt",
            f"{df['Tilt'].mean():.2f}°"
        )

    with sensor_col2:

        st.metric(
            "Average Displacement",
            f"{df['Displacement'].mean():.2f} mm"
        )

    with sensor_col3:

        st.metric(
            "Average Vibration",
            f"{df['Vibration'].mean():.2f} g"
        )

    with sensor_col4:

        st.metric(
            "Maximum Displacement",
            f"{df['Displacement'].max():.2f} mm"
        )

    st.divider()

    # =====================================================
    # SENSOR NETWORK
    # =====================================================

    st.subheader(
        "📡 Live Sensor Network"
    )

    display_df = df[
        [
            "Sensor",
            "Tilt",
            "Displacement",
            "Vibration",
            "Status"
        ]
    ].copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    st.divider()

    # =====================================================
    # AI PREDICTION
    # =====================================================

    st.subheader(
        "🤖 AI-Based Subsidence Prediction"
    )

    prediction_col1, prediction_col2 = (
        st.columns([2, 1])
    )

    with prediction_col1:

        if critical_count >= 5:

            st.error(
                "HIGH SUBSIDENCE RISK: Multiple "
                "nearby sensors indicate a developing "
                "deformation pattern."
            )

        elif warning_count >= 5:

            st.warning(
                "MODERATE SUBSIDENCE RISK: "
                "Localized deformation abnormalities "
                "are being detected."
            )

        else:

            st.info(
                "LOW SUBSIDENCE RISK: No significant "
                "deformation pattern detected."
            )

        st.write(
            "The proposed AI module analyses "
            "multi-sensor measurements such as "
            "tilt, displacement and vibration to "
            "identify abnormal deformation patterns "
            "and estimate future subsidence risk."
        )

    with prediction_col2:

        if critical_count >= 5:

            prediction = "HIGH"

        elif warning_count >= 5:

            prediction = "MEDIUM"

        else:

            prediction = "LOW"

        st.metric(
            "Predicted Risk",
            prediction
        )

        st.caption(
            "AI Prediction Module: Prototype"
        )

    st.divider()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    st.subheader(
        "🟢 System Status"
    )

    status_col1, status_col2, status_col3 = (
        st.columns(3)
    )

    with status_col1:

        st.success(
            "Sensor Network: ONLINE"
        )

    with status_col2:

        st.success(
            "Data Processing: ACTIVE"
        )

    with status_col3:

        st.success(
            "Early Warning: ACTIVE"
        )

    # =====================================================
    # LAST UPDATE
    # =====================================================

    st.divider()

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    st.caption(
        f"🔄 Live data • Last dashboard update: "
        f"{current_time}"
    )

    st.caption(
        "⚠️ Prototype simulation — sensor readings "
        "are synthetically generated and are not "
        "real mine measurements."
    )


# =========================================================
# RUN DASHBOARD
# =========================================================

live_dashboard()