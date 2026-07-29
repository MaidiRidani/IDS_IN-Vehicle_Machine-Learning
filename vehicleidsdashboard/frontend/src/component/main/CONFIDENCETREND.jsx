import Panel from "../common/Panel";
import { CLASS_INFO } from "../../constants/classInfo";

import {

    ResponsiveContainer,

    LineChart,

    Line,

    XAxis,

    YAxis,

    CartesianGrid,

    Tooltip,

    ReferenceLine,

} from "recharts";

function CONFIDENCETREND({

    history,

    className = "",

}) {

    const chartData =

        (history ?? []).map(

            (item, index) => ({

                window: index + 1,

                confidence: item.confidence,

                prediction: item.prediction,

                packet: item.packet_number,

            })

        );

    const confidenceLegend = [

        {

            title: "HIGH",

            desc: "≥95%",

            color: "#22C55E",

        },

        {

            title: "MEDIUM",

            desc: "80–94%",

            color: "#FACC15",

        },

        {

            title: "LOW",

            desc: "<80%",

            color: "#EF4444",

        },

    ];

    function CustomTooltip({

        active,

        payload,

    }) {

        if (

            !active ||

            !payload ||

            !payload.length

        ) {

            return null;

        }

        const item = payload[0].payload;
        

        return (

            <div
                className="
                    rounded-[8px]
                    border
                    border-white
                    bg-[#101B30]
                    px-[10px]
                    py-[8px]
                "
            >

                <p
                    className="
                        text-[11px]
                        font-bold
                    "
                    style={{

                        color:

                            CLASS_INFO[item.prediction].color,

                    }}
                >

                    {

                        CLASS_INFO[item.prediction]

                            .displayName

                    }

                </p>

                <p className="text-[10px]">

                    Window :

                    {" "}

                    {item.window}

                </p>

                <p className="text-[10px]">

                    Packet :

                    {" "}

                    {item.packet}

                </p>

                <p className="text-[10px]">

                    Confidence :

                    {" "}

                    {item.confidence}%

                </p>

            </div>

        );

    }

    return (

        <Panel
            className={`
                relative
                h-[278px]
                flex-1
                min-w-0
                ${className}
            `}
        >

            {/* Title */}

            <h2
                className="
                    absolute
                    text-[18px]
                    font-bold
                "
                style={{
                    left: "42px",
                    top: "20px",
                }}
            >
                CONFIDENCE TREND
            </h2>

            {/* ROC Placeholder */}

            <div
                className="
                    absolute
                    rounded-[10px]
                    border
                    border-white
                    flex
                    items-center
                    justify-center
                "
                style={{
                    left: "18px",
                    right: "95px",
                    top: "62px",
                    bottom: "16px",
                }}
            >

                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >

                    <LineChart

                        data={chartData}

                        margin={{

                            top: 10,

                            right: 10,

                            left: -18,

                            bottom: 5,

                        }}

                    >

                        <CartesianGrid
                            stroke="#334155"
                            strokeDasharray="3 3"
                        />
                        <ReferenceLine

                            y={95}

                            stroke="#22C55E"

                            strokeDasharray="4 4"

                            label={{


                                position:"insideRight",

                                fill:"#22C55E",


                            }}

                        />

                        <ReferenceLine

                            y={80}

                            stroke="#FACC15"

                            strokeDasharray="4 4"

                            label={{


                                position:"insideRight",

                                fill:"#FACC15",


                            }}

                        />

                        <ReferenceLine

                            y={60}

                            stroke="#EF4444"

                            strokeDasharray="4 4"

                            label={{


                                position:"insideRight",

                                fill:"#EF4444",


                            }}

                        />
                        <XAxis

                            dataKey="window"

                            tick={{

                                fill:"#CBD5E1",

                                fontSize:10,

                            }}

                        />

                        <YAxis

                            domain={[50, 100]}

                            ticks={[50,60,70, 80, 90,100]}

                            tick={{

                                fill:"#CBD5E1",

                                fontSize:10,

                            }}

                        />

                        <Tooltip

                            content={<CustomTooltip />}

                        />

                        <Line

                            type="monotone"

                            dataKey="confidence"

                            stroke="#2B9BFF"

                            strokeWidth={2}

                            isAnimationActive={false}

                            dot={(props) => {

                                const {

                                    cx,

                                    cy,

                                    payload,

                                } = props;

                                return (

                                    <circle

                                        cx={cx}

                                        cy={cy}

                                        r={4}

                                        fill={CLASS_INFO[payload.prediction].color}

                                        stroke="#FFFFFF"

                                        strokeWidth={1.2}

                                    />

                                );

                            }}
                                                    />

                    </LineChart>

                </ResponsiveContainer>
            </div>

            <div

                className="absolute"

                style={{
                    right: "12px",
                    top: "35px",
                }}

            >

                {

                    confidenceLegend.map((item, index)=>(

                        <div

                            key={item.title}

                            className="flex items-start mb-[22px]"

                        >

                            <div

                                className="rounded-full mt-[2px]"

                                style={{

                                    width:15,

                                    height:15,

                                    background:item.color,

                                }}

                            />

                            <div className="ml-[8px]">

                                <div

                                    className="text-[12px] font-semibold"

                                >

                                    {item.title}

                                </div>

                                <div

                                    className="text-[11px] text-slate-400"

                                >

                                    {item.desc}

                                </div>

                            </div>

                        </div>

                    ))

                }

            </div>


        </Panel>

    );

}

export default CONFIDENCETREND;