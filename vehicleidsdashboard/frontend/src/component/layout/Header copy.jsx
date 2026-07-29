import Panel from "../common/Panel";
import { metrics } from "../../config/headerConfig";
import { CLASS_INFO } from "../../constants/classInfo";

function Header({

    history = [],

}) {

    const labels = Object.keys(CLASS_INFO);

    // ================= CONFUSION MATRIX =================

    const matrix = {};

    labels.forEach(gt => {

        matrix[gt] = {};

        labels.forEach(pred => {

            matrix[gt][pred] = 0;

        });

    });

    history.forEach(item => {

        matrix[item.groundTruth][item.prediction]++;

    });

    // ================= ACCURACY =================

    let correct = 0;
    let total = 0;

    labels.forEach(gt => {

        labels.forEach(pred => {

            total += matrix[gt][pred];

            if (gt === pred) {

                correct += matrix[gt][pred];

            }

        });

    });

    const accuracy = total

        ? ((correct / total) * 100).toFixed(2)

        : "--";

    // ================= PRECISION =================

    const precisionList = [];

    labels.forEach(label => {

        const tp = matrix[label][label];

        let fp = 0;

        labels.forEach(gt => {

            if (gt !== label) {

                fp += matrix[gt][label];

            }

        });

        precisionList.push(

            tp + fp

                ? tp / (tp + fp)

                : 0

        );

    });

    const macroPrecision = (

        precisionList.reduce(

            (a, b) => a + b,

            0

        ) / labels.length * 100

    ).toFixed(2);

    // ================= RECALL =================

    const recallList = [];

    labels.forEach(label => {

        const tp = matrix[label][label];

        let fn = 0;

        labels.forEach(pred => {

            if (pred !== label) {

                fn += matrix[label][pred];

            }

        });

        recallList.push(

            tp + fn

                ? tp / (tp + fn)

                : 0

        );

    });

    const macroRecall = (

        recallList.reduce(

            (a, b) => a + b,

            0

        ) / labels.length * 100

    ).toFixed(2);

    // ================= F1 =================

    const macroF1 = (

        precisionList.map((p, i) => {

            const r = recallList[i];

            return (p + r)

                ? (2 * p * r) / (p + r)

                : 0;

        }).reduce(

            (a, b) => a + b,

            0

        ) / labels.length * 100

    ).toFixed(2);

    // ================= LAST RESULT =================

    const lastHistory = history.at(-1);

    const latencyMs =

        lastHistory?.average_latency_ms ?? null;

    const latencySeconds =

        latencyMs !== null

            ? (latencyMs / 1000).toFixed(4)

            : "--";

    // ================= VALUES =================

    const values = {

        accuracy: `${accuracy}%`,

        precision: `${macroPrecision}%`,

        recall: `${macroRecall}%`,

        f1: `${macroF1}%`,

        inference:

            latencyMs !== null

                ? `${latencyMs} ms`

                : "--",

        confidence:

            lastHistory

                ? `${lastHistory.confidence}%`

                : "--",

    };

    return (

        <Panel className="h-[129px] w-full px-5 flex items-center">

            {/* Logo */}

            <img

                src="/icon/logopojok.svg"

                alt="Logo"

                className="h-[96px] w-auto object-contain"

            />

            {/* Metric Cards */}

            <div className="ml-[6.5px] flex">

                {

                    metrics.map(item => (

                        <div

                            key={item.id}

                            className="
                                relative
                                border
                                border-[#243552]
                                flex
                                items-center
                                transition-all
                                duration-300
                            "

                            style={{

                                width: item.card.width,

                                height: item.card.height,

                                marginLeft: item.card.marginLeft,

                                borderRadius: item.card.radius,

                                background: item.card.background,

                            }}

                        >

                            <img

                                src={item.icon}

                                alt={item.id}

                                className="object-contain"

                                style={{

                                    width: item.image.width,

                                    height: item.image.height,

                                    marginLeft: item.image.marginLeft,

                                    marginTop: item.image.marginTop,

                                }}

                            />

                            <div

                                style={{

                                    position: "absolute",

                                    left: item.titleStyle.left,

                                    top: item.titleStyle.top,

                                    fontSize: item.titleStyle.fontSize,

                                    fontWeight: item.titleStyle.fontWeight,

                                    fontFamily: "Inter",

                                    whiteSpace: "pre-line",

                                }}

                            >

                                {item.title}

                            </div>

                            <div

                                style={{

                                    position: "absolute",

                                    left: item.valueStyle.left,

                                    top: item.valueStyle.top,

                                    fontSize: item.valueStyle.fontSize,

                                    fontWeight: item.valueStyle.fontWeight,

                                }}

                            >

                                {values[item.id]}

                            </div>

                            {
                                item.id === "inference" && latencyMs !== null && (
                                    <div
                                        className="absolute text-[10px] text-[#94A3B8] mt-2"
                                        style={{
                                            left: item.valueStyle.left,
                                            top: item.valueStyle.top + 20,
                                        }}
                                    >
                                        {latencySeconds} sec
                                    </div>
                                )
                            }

                        </div>

                    ))

                }

            </div>

        </Panel>

    );

}

export default Header;