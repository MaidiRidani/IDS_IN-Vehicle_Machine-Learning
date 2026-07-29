export const metrics = [
    {
        id: "accuracy",
        title: "ACCURACY",
        icon: "/icon/accuracy.svg",

        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "95.34%",      // Accuracy

        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 6.5,    
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 10,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },      
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },

    {
        id: "precision",
        title: "PRECISION",
        icon: "/icon/precision.svg",

        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "94.82%",      // Precision

        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 0,
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 6,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },

    {
        id: "recall",
        title: "RECALL",
        icon: "/icon/recall.svg",

        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "96.12%",      // Recall

        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 0,
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 9,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },

    {
        id: "f1",
        title: "F1-SCORE",
        icon: "/icon/f1-score.svg",


        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "95.47%",      // F1-Score

        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 0,
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 9,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },

    {
        id: "inference",
        title: "INFERENCE\nTIME",
        icon: "/icon/inferencetime.svg",

        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "0.12s",      // Inference Time


        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 0,
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 7,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },

    {
        id: "confidence",
        title: "CONFIDENCE\nLAST",
        icon: "/icon/confidence.svg",

        // Placeholder
        // TODO: Value ini nanti diganti dari backend Python (FastAPI)
        value: "92.76%",      // Confidence Last

        card: {
            width: 190,
            height: 106,
            radius: 10,
            marginLeft: 0,
            background: "#070E1B",
        },

        image: {
            width: "auto",
            height: 106,
            marginLeft: 7,
            marginTop: 0,
        },
        titleStyle:{

            left:95,

            top:10,

            fontSize:12,

            fontWeight:700,

        },
        valueStyle:{

            left:95,

            top:50,

            fontSize:20,

            fontWeight:700,

        },
    },
];