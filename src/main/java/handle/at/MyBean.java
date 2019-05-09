package handle.at;

public class MyBean {
    @MyAnnotation(30)
    private int value;
    @Override
    public String toString() {
        return String.valueOf(value);
    }
}