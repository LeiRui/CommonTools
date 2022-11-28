package tools;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class FindRegularTimeInterval {

  public static void main(String[] args) throws Exception {
    String csvData = "D:\\github\\now\\MF03.csv";
    boolean hasHeader = true;
//    DescriptiveStatistics intervals = new DescriptiveStatistics();
    Map<Long, Integer> intervalMap = new HashMap<>();
    int totalCount = 0;
    try (BufferedReader br = new BufferedReader(new FileReader(csvData))) {
      if (hasHeader) {
        br.readLine();
      }
      long lastTimestamp = -1;
      for (String line; (line = br.readLine()) != null; ) {
        String[] tv = line.split(",");
        long time = Long.parseLong(tv[0]); // get timestamp from real data
        if (lastTimestamp > 0) {
          long interval = time - lastTimestamp;
          if (intervalMap.containsKey(interval)) {
            intervalMap.put(interval, intervalMap.get(interval) + 1);
          } else {
            intervalMap.put(interval, 1);
          }
          totalCount++;
        }
        lastTimestamp = time;
      }
    }

    List<Entry<Long, Integer>> nlist = new ArrayList<>(intervalMap.entrySet());
    nlist.sort(Entry.comparingByValue());
//    nlist.forEach(System.out::println);
    for (Entry entry : nlist) {
      System.out.println(
          entry.getKey() + ": " + entry.getValue() + ", "
              + (int) entry.getValue() * 1.0 / totalCount * 100
              + "%");
    }
  }

}
