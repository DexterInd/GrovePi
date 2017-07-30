package org.iot.raspberry.grovepi;

import java.io.IOException;

public interface GrovePiSequence<T> {

  T execute(GroveIO io) throws IOException;

}
