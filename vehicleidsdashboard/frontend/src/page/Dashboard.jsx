// import DashboardLayout from "../component/layout/DashboardLayout";

// function Dashboard() {
//     return <DashboardLayout />;
// }

// export default Dashboard;

// import { useEffect } from "react";

// import DashboardLayout from "../component/layout/DashboardLayout";
// import { getDatasets } from "../api/preprocessing";

// function Dashboard() {

//     useEffect(() => {

//         getDatasets()
//             .then(data => console.log(data))
//             .catch(error => console.error(error));

//     }, []);

//     return <DashboardLayout />;

// }

// export default Dashboard;



import { useEffect } from "react";

import DashboardLayout from "../component/layout/DashboardLayout";
import { getModels, loadModel } from "../api/detection";

function Dashboard() {

    useEffect(() => {

        async function test() {

            try {

                const models = await getModels();

                console.log(models);

                const info = await loadModel(models[0]);

                console.log(info);

            } catch (error) {

                console.error(error);

            }

        }

        test();

    }, []);

    return <DashboardLayout />;

}

export default Dashboard;
