from current import TEMPLATE as BASE

_lombok_header = """
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
{header}
@AllArgsConstructor
@Builder
@Data
@NoArgsConstructor"""

TEMPLATE = BASE.replace('{header}', _lombok_header)
