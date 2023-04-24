import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import com.opencsv.CSVWriter;

/**
 * @author Weiqi Hu
 * @create 2023-04-19 18:06
 */
public class App {
    static double[][] dis = new double[16][16];
    static int[][] next = new int[16][16];
    static int INF = (int) 1e7;
    static int doubledNum = 0;
    static HashMap<ArrayList<Integer>, Double> optimizedPathAvgThroughputMap = new HashMap<>();
    static HashMap<ArrayList<Integer>, Double> optimizedPathAvgOriginalThroughputMap = new HashMap<>();
    static final Map<Integer, String> constant = new HashMap<>() {{
        put(0, "AZURE_US_EAST");
        put(1, "AZURE_FRANCE_CENTRAL");
        put(2, "AZURE_JAPAN_EAST");
        put(3, "AZURE_BRAZIL_SOUTH");
        put(4, "AZURE_SOUTH_AFRICA_NORTH");
        put(5, "GCP_US_CENTRAL_1");
        put(6, "GCP_EUROPE_NORTH_1");
        put(7, "AWS_SA_EAST_1_SAO_PAULO");
        put(8, "GCP_ASIA_EAST_1");
        put(9, "AWS_US_EAST_2_OHIO");
        put(10, "GCP_AUSTRALIA_SOUTHEAST_1");
        put(11, "GCP_US_SOUTH_1");
        put(12, "AWS_US_WEST_1_CALIFORNIA");
        put(13, "AWS_US_WEST_2_OREGON");
        put(14, "AWS_EU_CENTRAL_1_FRANKFURT");
        put(15, "AWS_EU_NORTH_1_STOCKHOLM");
    }};


    static void initialise(int V, double[][] graph) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                dis[i][j] = graph[i][j];

                // No edge between node
                // i and j
                if (graph[i][j] == INF)
                    next[i][j] = -1;
                else
                    next[i][j] = j;
            }
        }
    }

    static void floydWarshall(int V) {
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {

                    // We cannot travel through
                    // edge that doesn't exist
                    if (dis[i][k] == INF ||
                            dis[k][j] == INF)
                        continue;

                    if (i == j) continue;

                    if (dis[i][j] > dis[i][k] +
                            dis[k][j]) {
                        dis[i][j] = dis[i][k] +
                                dis[k][j];
                        next[i][j] = next[i][k];
                    }
                }
            }
        }
    }

    static String[][] printOptimizedData(HashMap<ArrayList<Integer>, Integer> optimizedPathCountMap) {
        String[][] res = new String[optimizedPathCountMap.size()][4];

        List<Map.Entry<ArrayList<Integer>, Integer>> list = new ArrayList<>(optimizedPathCountMap.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<ArrayList<Integer>, Integer>>() {
            public int compare(Map.Entry<ArrayList<Integer>, Integer> o1, Map.Entry<ArrayList<Integer>, Integer> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        int i = 0;
        for (Map.Entry<ArrayList<Integer>, Integer> entry : list) {
            final double avgThroughput = optimizedPathAvgThroughputMap.get(entry.getKey()) / entry.getValue();

            final double avgOriginalThroughput = optimizedPathAvgOriginalThroughputMap.get(entry.getKey()) / entry.getValue();
            final double avgPercentOptimized = 100 * ((avgThroughput - avgOriginalThroughput) / avgOriginalThroughput);
            final double avgOptimizedLatency = (avgThroughput - avgOriginalThroughput) / 1024;
            res[i++] = new String[]{printPath(entry.getKey()).substring(0, printPath(entry.getKey()).length() - 1), String.valueOf(entry.getValue()), String.valueOf(avgPercentOptimized), String.valueOf(avgOptimizedLatency)};
        }

        return res;
    }

    static ArrayList<Integer> constructPath(int u, int v) {

        // If there's no path between
        // node u and v, simply return
        // an empty array
        if (next[u][v] == -1)
            return null;

        // Storing the path in a vector
        ArrayList<Integer> path = new ArrayList<Integer>();
        path.add(u);

        while (u != v) {
            u = next[u][v];
            path.add(u);
        }
        return path;
    }

    static String printPath(ArrayList<Integer> path) {
        final StringBuilder output = new StringBuilder();
        int n = path.size();
        for (int i = 0; i < n - 1; i++) {
            output.append(constant.get((path.get(i))) + " -> ");
        }
        output.append(
                constant.get(path.get(n - 1)) + "\n");
        return output.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader reader;
        int count = 0;
        final HashMap<ArrayList<Integer>, Integer> optimizedPathCountMap = new HashMap<>();
        final HashMap<Integer, Integer> pathHopCountMap = new HashMap<>();
        int paths_already_optimized = 0;
        try {
            reader = new BufferedReader(new FileReader("/Users/huweiqi/IdeaProjects/ThroughputOptimizer/part-r-00000"));
            String line = reader.readLine();
            while (line != null) {
                if (line.contains("Start_Of")) {
                    double[][] graph = new double[16][16];

                    for (int i = 0; i < 16; i++) {
                        line = reader.readLine();
                        String[] row = line.split(",");
                        for (int j = 0; j < row.length; j++) {
                            if (row[j].equals(" null")) {
                                graph[i][j] = INF;
                            } else {
                                graph[i][j] = 1100009.0 / Double.parseDouble(row[j]);
                            }
                        }

                    }

                    initialise(16, graph);
                    floydWarshall(16);
                    ArrayList<Integer> path;

                    for (int k = 0; k < 16; k++) {
                        for (int l = 0; l < 16; l++) {
                            if (k == l || graph[k][l] == INF) continue;
                            path = constructPath(k, l);
                            if (path.size() > 2) {
                                if (optimizedPathCountMap.get(path) != null) {
                                    optimizedPathCountMap.put(path, optimizedPathCountMap.get(path) + 1);
                                } else {
                                    optimizedPathCountMap.put(path, 1);
                                }

                                if (pathHopCountMap.get(path.size()) != null) {
                                    pathHopCountMap.put(path.size(), pathHopCountMap.get(path.size()) + 1);
                                } else {
                                    pathHopCountMap.put(path.size(), 1);
                                }

                                double percentOptimized = 100 * ((1100009.0 / dis[k][l] - 1100009.0 / graph[k][l]) / (1100009.0 / graph[k][l]));
                                if (percentOptimized >= 50) doubledNum++;

                                optimizedPathAvgThroughputMap.put(path, optimizedPathAvgThroughputMap.getOrDefault(path, 0.0) + 1100009.0 / dis[k][l]);
                                optimizedPathAvgOriginalThroughputMap.put(path, optimizedPathAvgOriginalThroughputMap.getOrDefault(path, 0.0) + 1100009.0 / graph[k][l]);
                            } else {
                                ++paths_already_optimized;
                            }
                            count++;
                        }
                    }
                }

                // read next line
                line = reader.readLine();
            }


            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

//        System.out.println("total paths: " + count);
        System.out.println("Paths already optimized: " + paths_already_optimized + "\n");
        for (final Map.Entry<Integer, Integer> entry : pathHopCountMap.entrySet()) {
            System.out.println(
                    "Additional Hops: " + (entry.getKey() - 2) + " Number of paths: " + entry.getValue() + "\n");
        }


        CSVWriter writer = new CSVWriter(new FileWriter("data.csv"), CSVWriter.DEFAULT_SEPARATOR ,CSVWriter.NO_QUOTE_CHARACTER, CSVWriter.DEFAULT_ESCAPE_CHARACTER, CSVWriter.DEFAULT_LINE_END);
        String[] header = {"path","times_optimized","avg_percent_optimized","avg_optimized_throughput_kb/s"};
        writer.writeNext(header);

        String[][] temp = printOptimizedData(optimizedPathCountMap);
        for (String[] s : temp) {
            writer.writeNext(s);
        }

        writer.close();

        System.out.println("Total paths: " + count);
        System.out.println("Throughput doubled count: " + doubledNum);
    }
}
