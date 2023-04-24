package floyd.warshall;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Vector;

public class helpers {
    public static double[][] readDocument(final String input_path) {
        double[][] graph = new double[constants.NUM_NODES][constants.NUM_NODES];
        try (FileReader fr = new FileReader(input_path)) {
            final BufferedReader bufferedReader = new BufferedReader(fr);
            String line = null;
            int i = 0;
            while ((line = bufferedReader.readLine()) != null) {
                final String[] lineArray = line.split(",");
                for (int j = 0; j < lineArray.length; ++j) {
                    graph[i][j] = Double.parseDouble(lineArray[j]);
                }
                ++i;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return graph;
    }

    // Ripped from geeks for geeks
    // https://www.geeksforgeeks.org/sorting-a-hashmap-according-to-values/
    public static HashMap<Vector<Integer>, Integer> sortByValue(HashMap<Vector<Integer>, Integer> hm) {
        // Create a list from elements of HashMap
        List<Map.Entry<Vector<Integer>, Integer>> list = new LinkedList<>(hm.entrySet());

        // Sort the list using lambda expression
        Collections.sort(
                list,
                (i1,
                        i2) -> i2.getValue().compareTo(i1.getValue()));

        // put data from sorted list to hashmap
        HashMap<Vector<Integer>, Integer> temp = new LinkedHashMap<>();
        for (Map.Entry<Vector<Integer>, Integer> aa : list) {
            temp.put(aa.getKey(), aa.getValue());
        }
        return temp;
    }

    public static double[][] readGraphFromOpenDocument(final BufferedReader openBufferedReader)
            throws NumberFormatException, IOException {
        double[][] graph = new double[constants.NUM_NODES][constants.NUM_NODES];
        String line = null;
        int i = 0;
        if ((line = openBufferedReader.readLine()) == null)
            return null;
        if (line.contains("---Start")) {
            // Read next line until ---end_of_i--- reached
            while (!(line = openBufferedReader.readLine()).contains("---End")) {
                final String[] lineArray = line.split(",");
                for (int j = 0; j < lineArray.length; ++j) {
                    graph[i][j] = Double.parseDouble(lineArray[j]);
                }
                ++i;
            }
        } else {
            // throw new IOException("Error reading distance matrix");
            return null;
        }
        // skip newline added from reducer
        openBufferedReader.readLine();
        return graph;
    }
}
