const BASE = import.meta.env.BASE_URL;

const STORAGE_KEY = "netshield_records_v1";


// ==========================================
// LOAD JSON DATA
// ==========================================

async function loadJSON(filename) {

  const response = await fetch(
    `${BASE}data/${filename}`
  );

  if (!response.ok) {
    throw new Error(`Unable to load ${filename}`);
  }

  return response.json();
}


// ==========================================
// BROWSER LOCAL STORAGE
// ==========================================

function getRecords() {

  try {
    return JSON.parse(
      localStorage.getItem(STORAGE_KEY) || "[]"
    );
  } catch {
    return [];
  }

}


function saveRecords(records) {

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(records)
  );

}


// ==========================================
// LOCAL API
// ==========================================

const localApi = {

  async get(url) {

    const endpoint = url.split("/").pop();

    const records = getRecords();

    switch (endpoint) {

      case "health":

        return {
          data: {
            status: "healthy",
            mode: "Browser demonstration",
            timestamp: new Date().toISOString()
          }
        };


      case "statistics":

        return {
          data: {
            total_flows: records.length,

            benign_flows: records.filter(
              r => r.label === "BENIGN"
            ).length,

            flagged_flows: records.filter(
              r => r.label === "ATTACK"
            ).length
          }
        };


      case "flows":

        return {
          data: records
        };


      case "alerts":

        return {
          data: records.filter(
            r => r.label === "ATTACK"
          )
        };


      case "model":

        return {
          data: await loadJSON("metrics.json")
        };


      case "validation":

        return {
          data: await loadJSON("validation.json")
        };


      default:

        throw new Error(
          `Unknown endpoint: ${endpoint}`
        );

    }

  },


  async post(url) {

    const endpoint = url.split("/").pop();

    if (endpoint !== "analyze") {
      throw new Error("Unknown operation");
    }

    const predictions = await loadJSON(
      "predictions.json"
    );

    const existing = getRecords();

    const nextId = existing.reduce(
      (max, record) => Math.max(max, record.id),
      0
    ) + 1;

    const newRecords = predictions.map(
      (prediction, index) => ({

        ...prediction,

        id: nextId + index,

        timestamp: new Date().toISOString()

      })
    );

    saveRecords([
      ...newRecords.reverse(),
      ...existing
    ].slice(0, 500));

    return {
      data: {
        status: "success",
        processed: newRecords.length
      }
    };

  }

};

export default localApi;