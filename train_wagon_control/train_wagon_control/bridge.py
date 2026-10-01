# Bridge between the UI (HTML/JS) and the doubly linked list in Python.
# Replies carry message keys; the UI turns them into text.
import json

train = Train()
_dump = json.dumps


def _state(ok=True, msg="", params=None, code="", new_id=None):
    wagons = []
    node = train.head
    while node is not None:
        wagons.append({
            "id": node.id, "type": node.type, "cargo": node.cargo,
            "prev": node.prev.id if node.prev else None,
            "next": node.next.id if node.next else None,
        })
        node = node.next
    return json.dumps({
        "ok": ok, "msg": msg, "params": params or {}, "code": code, "new_id": new_id,
        "wagons": wagons, "length": train.length,
        "head": train.head.id if train.head else None,
        "tail": train.tail.id if train.tail else None,
        "current_id": train.current.id if train.current else None,
        "current_index": train.index_of(train.current) if train.current else -1,
    })


def handle(action, payload_json):
    global train
    data = json.loads(payload_json or "{}")
    try:
        if action == "append":
            wagon = train.append(data["wagon_type"], data["cargo"])
            train.current = wagon
            return _state(msg="appended", params={"id": wagon.id}, new_id=wagon.id,
                          code=f"train.append({_dump(data['wagon_type'])}, {_dump(data['cargo'])})")
        if action == "prepend":
            wagon = train.prepend(data["wagon_type"], data["cargo"])
            train.current = wagon
            return _state(msg="prepended", params={"id": wagon.id}, new_id=wagon.id,
                          code=f"train.prepend({_dump(data['wagon_type'])}, {_dump(data['cargo'])})")
        if action == "insert":
            index = int(data["index"])
            out_of_range = train.length > 0 and index >= train.length
            wagon = train.insert(index, data["wagon_type"], data["cargo"])
            train.current = wagon
            msg = "inserted_out_of_range" if out_of_range else "inserted"
            return _state(msg=msg,
                          params={"id": wagon.id, "index": train.index_of(wagon), "requested": index},
                          new_id=wagon.id,
                          code=f"train.insert({index}, {_dump(data['wagon_type'])}, {_dump(data['cargo'])})")
        if action == "remove_current":
            if train.current is None:
                return _state(False, "nothing_to_remove")
            index = train.index_of(train.current)
            wagon = train.remove(index)
            return _state(msg="removed", params={"id": wagon.id}, code=f"train.remove({index})")
        if action == "next":
            moved = train.go_next()
            return _state(moved, "moved_next" if moved else "at_tail", code="train.go_next()" if moved else "")
        if action == "prev":
            moved = train.go_prev()
            return _state(moved, "moved_prev" if moved else "at_head", code="train.go_prev()" if moved else "")
        if action == "head":
            train.go_head()
            return _state(msg="selected_head", code="train.go_head()")
        if action == "tail":
            train.go_tail()
            return _state(msg="selected_tail", code="train.go_tail()")
        if action == "select":
            index = int(data["index"])
            train.current = train.traverse_to_index(index)
            return _state(msg="selected", params={"id": train.current.id},
                          code=f"train.traverse_to_index({index})")
        if action == "reset":
            train = Train()
            return _state(msg="empty_train", code="train = Train()")
        if action == "demo":
            train = Train()
            for item in data["wagons"]:
                train.append(item["wagon_type"], item["cargo"])
            train.go_head()
            return _state(msg="demo_loaded",
                          code=f"train = Train()\ntrain.append(...)  # x{train.length} wagons")
        return _state(False, "unknown_action")
    except IndexError:
        return _state(False, "no_wagon_at_position")
    except (ValueError, KeyError, TypeError):
        return _state(False, "invalid_data")
