@Component
public class SomeService{

    private final Cache cache;

    @AutoWired
    public SomeService(Cache cache){
        this.cache = cache;
    }
}