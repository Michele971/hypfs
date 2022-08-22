// Automatically generated with Reach 0.1.11 (27cb9643)
pragma abicoder v2;

pragma solidity ^0.8.12;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
    /**
     * @dev Returns the amount of tokens in existence.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns the amount of tokens owned by `account`.
     */
    function balanceOf(address account) external view returns (uint256);

    /**
     * @dev Moves `amount` tokens from the caller's account to `to`.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transfer(address to, uint256 amount) external returns (bool);

    /**
     * @dev Returns the remaining number of tokens that `spender` will be
     * allowed to spend on behalf of `owner` through {transferFrom}. This is
     * zero by default.
     *
     * This value changes when {approve} or {transferFrom} are called.
     */
    function allowance(address owner, address spender) external view returns (uint256);

    /**
     * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * IMPORTANT: Beware that changing an allowance with this method brings the risk
     * that someone may use both the old and the new allowance by unfortunate
     * transaction ordering. One possible solution to mitigate this race
     * condition is to first reduce the spender's allowance to 0 and set the
     * desired value afterwards:
     * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
     *
     * Emits an {Approval} event.
     */
    function approve(address spender, uint256 amount) external returns (bool);

    /**
     * @dev Moves `amount` tokens from `from` to `to` using the
     * allowance mechanism. `amount` is then deducted from the caller's
     * allowance.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);

    /**
     * @dev Emitted when `value` tokens are moved from one account (`from`) to
     * another (`to`).
     *
     * Note that `value` may be zero.
     */
    event Transfer(address indexed from, address indexed to, uint256 value);

    /**
     * @dev Emitted when the allowance of a `spender` for an `owner` is set by
     * a call to {approve}. `value` is the new allowance.
     */
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

/**
 * @dev Interface for the optional metadata functions from the ERC20 standard.
 *
 * _Available since v4.1._
 */
interface IERC20Metadata is IERC20 {
    /**
     * @dev Returns the name of the token.
     */
    function name() external view returns (string memory);

    /**
     * @dev Returns the symbol of the token.
     */
    function symbol() external view returns (string memory);

    /**
     * @dev Returns the decimals places of the token.
     */
    function decimals() external view returns (uint8);
}

/**
 * @dev Provides information about the current execution context, including the
 * sender of the transaction and its data. While these are generally available
 * via msg.sender and msg.data, they should not be accessed in such a direct
 * manner, since when dealing with meta-transactions the account sending and
 * paying for execution may not be the actual sender (as far as an application
 * is concerned).
 *
 * This contract is only required for intermediate, library-like contracts.
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}

/**
 * @dev Implementation of the {IERC20} interface.
 *
 * This implementation is agnostic to the way tokens are created. This means
 * that a supply mechanism has to be added in a derived contract using {_mint}.
 * For a generic mechanism see {ERC20PresetMinterPauser}.
 *
 * TIP: For a detailed writeup see our guide
 * https://forum.zeppelin.solutions/t/how-to-implement-erc20-supply-mechanisms/226[How
 * to implement supply mechanisms].
 *
 * We have followed general OpenZeppelin Contracts guidelines: functions revert
 * instead returning `false` on failure. This behavior is nonetheless
 * conventional and does not conflict with the expectations of ERC20
 * applications.
 *
 * Additionally, an {Approval} event is emitted on calls to {transferFrom}.
 * This allows applications to reconstruct the allowance for all accounts just
 * by listening to said events. Other implementations of the EIP may not emit
 * these events, as it isn't required by the specification.
 *
 * Finally, the non-standard {decreaseAllowance} and {increaseAllowance}
 * functions have been added to mitigate the well-known issues around setting
 * allowances. See {IERC20-approve}.
 */
contract ERC20 is Context, IERC20, IERC20Metadata {
    mapping(address => uint256) private _balances;

    mapping(address => mapping(address => uint256)) private _allowances;

    uint256 private _totalSupply;

    string private _name;
    string private _symbol;

    /**
     * @dev Sets the values for {name} and {symbol}.
     *
     * The default value of {decimals} is 18. To select a different value for
     * {decimals} you should overload it.
     *
     * All two of these values are immutable: they can only be set once during
     * construction.
     */
    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
    }

    /**
     * @dev Returns the name of the token.
     */
    function name() public view virtual override returns (string memory) {
        return _name;
    }

    /**
     * @dev Returns the symbol of the token, usually a shorter version of the
     * name.
     */
    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }

    /**
     * @dev Returns the number of decimals used to get its user representation.
     * For example, if `decimals` equals `2`, a balance of `505` tokens should
     * be displayed to a user as `5.05` (`505 / 10 ** 2`).
     *
     * Tokens usually opt for a value of 18, imitating the relationship between
     * Ether and Wei. This is the value {ERC20} uses, unless this function is
     * overridden;
     *
     * NOTE: This information is only used for _display_ purposes: it in
     * no way affects any of the arithmetic of the contract, including
     * {IERC20-balanceOf} and {IERC20-transfer}.
     */
    function decimals() public view virtual override returns (uint8) {
        return 18;
    }

    /**
     * @dev See {IERC20-totalSupply}.
     */
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    /**
     * @dev See {IERC20-balanceOf}.
     */
    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    /**
     * @dev See {IERC20-transfer}.
     *
     * Requirements:
     *
     * - `to` cannot be the zero address.
     * - the caller must have a balance of at least `amount`.
     */
    function transfer(address to, uint256 amount) public virtual override returns (bool) {
        address owner = _msgSender();
        _transfer(owner, to, amount);
        return true;
    }

    /**
     * @dev See {IERC20-allowance}.
     */
    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return _allowances[owner][spender];
    }

    /**
     * @dev See {IERC20-approve}.
     *
     * NOTE: If `amount` is the maximum `uint256`, the allowance is not updated on
     * `transferFrom`. This is semantically equivalent to an infinite approval.
     *
     * Requirements:
     *
     * - `spender` cannot be the zero address.
     */
    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        address owner = _msgSender();
        _approve(owner, spender, amount);
        return true;
    }

    /**
     * @dev See {IERC20-transferFrom}.
     *
     * Emits an {Approval} event indicating the updated allowance. This is not
     * required by the EIP. See the note at the beginning of {ERC20}.
     *
     * NOTE: Does not update the allowance if the current allowance
     * is the maximum `uint256`.
     *
     * Requirements:
     *
     * - `from` and `to` cannot be the zero address.
     * - `from` must have a balance of at least `amount`.
     * - the caller must have allowance for ``from``'s tokens of at least
     * `amount`.
     */
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) public virtual override returns (bool) {
        address spender = _msgSender();
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        return true;
    }

    /**
     * @dev Atomically increases the allowance granted to `spender` by the caller.
     *
     * This is an alternative to {approve} that can be used as a mitigation for
     * problems described in {IERC20-approve}.
     *
     * Emits an {Approval} event indicating the updated allowance.
     *
     * Requirements:
     *
     * - `spender` cannot be the zero address.
     */
    function increaseAllowance(address spender, uint256 addedValue) public virtual returns (bool) {
        address owner = _msgSender();
        _approve(owner, spender, _allowances[owner][spender] + addedValue);
        return true;
    }

    /**
     * @dev Atomically decreases the allowance granted to `spender` by the caller.
     *
     * This is an alternative to {approve} that can be used as a mitigation for
     * problems described in {IERC20-approve}.
     *
     * Emits an {Approval} event indicating the updated allowance.
     *
     * Requirements:
     *
     * - `spender` cannot be the zero address.
     * - `spender` must have allowance for the caller of at least
     * `subtractedValue`.
     */
    function decreaseAllowance(address spender, uint256 subtractedValue) public virtual returns (bool) {
        address owner = _msgSender();
        uint256 currentAllowance = _allowances[owner][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        unchecked {
            _approve(owner, spender, currentAllowance - subtractedValue);
        }

        return true;
    }

    /**
     * @dev Moves `amount` of tokens from `sender` to `recipient`.
     *
     * This internal function is equivalent to {transfer}, and can be used to
     * e.g. implement automatic token fees, slashing mechanisms, etc.
     *
     * Emits a {Transfer} event.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `from` must have a balance of at least `amount`.
     */
    function _transfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");

        _beforeTokenTransfer(from, to, amount);

        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: transfer amount exceeds balance");
        unchecked {
            _balances[from] = fromBalance - amount;
        }
        _balances[to] += amount;

        emit Transfer(from, to, amount);

        _afterTokenTransfer(from, to, amount);
    }

    /** @dev Creates `amount` tokens and assigns them to `account`, increasing
     * the total supply.
     *
     * Emits a {Transfer} event with `from` set to the zero address.
     *
     * Requirements:
     *
     * - `account` cannot be the zero address.
     */
    function _mint(address account, uint256 amount) internal virtual {
        require(account != address(0), "ERC20: mint to the zero address");

        _beforeTokenTransfer(address(0), account, amount);

        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);

        _afterTokenTransfer(address(0), account, amount);
    }

    /**
     * @dev Destroys `amount` tokens from `account`, reducing the
     * total supply.
     *
     * Emits a {Transfer} event with `to` set to the zero address.
     *
     * Requirements:
     *
     * - `account` cannot be the zero address.
     * - `account` must have at least `amount` tokens.
     */
    function _burn(address account, uint256 amount) internal virtual {
        require(account != address(0), "ERC20: burn from the zero address");

        _beforeTokenTransfer(account, address(0), amount);

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "ERC20: burn amount exceeds balance");
        unchecked {
            _balances[account] = accountBalance - amount;
        }
        _totalSupply -= amount;

        emit Transfer(account, address(0), amount);

        _afterTokenTransfer(account, address(0), amount);
    }

    /**
     * @dev Sets `amount` as the allowance of `spender` over the `owner` s tokens.
     *
     * This internal function is equivalent to `approve`, and can be used to
     * e.g. set automatic allowances for certain subsystems, etc.
     *
     * Emits an {Approval} event.
     *
     * Requirements:
     *
     * - `owner` cannot be the zero address.
     * - `spender` cannot be the zero address.
     */
    function _approve(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    /**
     * @dev Spend `amount` form the allowance of `owner` toward `spender`.
     *
     * Does not update the allowance amount in case of infinite allowance.
     * Revert if not enough allowance is available.
     *
     * Might emit an {Approval} event.
     */
    function _spendAllowance(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {
        uint256 currentAllowance = allowance(owner, spender);
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "ERC20: insufficient allowance");
            unchecked {
                _approve(owner, spender, currentAllowance - amount);
            }
        }
    }

    /**
     * @dev Hook that is called before any transfer of tokens. This includes
     * minting and burning.
     *
     * Calling conditions:
     *
     * - when `from` and `to` are both non-zero, `amount` of ``from``'s tokens
     * will be transferred to `to`.
     * - when `from` is zero, `amount` tokens will be minted for `to`.
     * - when `to` is zero, `amount` of ``from``'s tokens will be burned.
     * - `from` and `to` are never both zero.
     *
     * To learn more about hooks, head to xref:ROOT:extending-contracts.adoc#using-hooks[Using Hooks].
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual {}

    /**
     * @dev Hook that is called after any transfer of tokens. This includes
     * minting and burning.
     *
     * Calling conditions:
     *
     * - when `from` and `to` are both non-zero, `amount` of ``from``'s tokens
     * has been transferred to `to`.
     * - when `from` is zero, `amount` tokens have been minted for `to`.
     * - when `to` is zero, `amount` of ``from``'s tokens have been burned.
     * - `from` and `to` are never both zero.
     *
     * To learn more about hooks, head to xref:ROOT:extending-contracts.adoc#using-hooks[Using Hooks].
     */
    function _afterTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual {}
}
/*
  ReachToken essentially emulates Algorand Standard Assets on Ethereum, but doesn't include things like clawback or a separation of management and creator.
 */
contract ReachToken is ERC20 {
  address private _creator;
  string private _url;
  string private _metadata;
  uint8 private _decimals;

  constructor (
    string memory name_,
    string memory symbol_,
    string memory url_,
    string memory metadata_,
    uint256 supply_,
    uint256 decimals_
  ) ERC20(name_, symbol_) {
    _creator = _msgSender();
    _mint(_creator, supply_);
    _url = url_;
    _metadata = metadata_;
    _decimals = uint8(decimals_);
  }

  function url() public view returns (string memory) { return _url; }

  function metadata() public view returns (string memory) { return _metadata; }

  function decimals() public view override returns (uint8) { return _decimals; }

  function burn(uint256 amount) public virtual returns (bool) {
    require(_msgSender() == _creator, "must be creator");
    _burn(_creator, amount);
    return true;
  }

  function destroy() public virtual {
    require(_msgSender() == _creator, "must be creator");
    require(totalSupply() == 0, "must be no supply");
    selfdestruct(payable(_creator));
  }
}

// Generated code includes meaning of numbers
error ReachError(uint256 msg);

contract Stdlib {
  function safeAdd(uint256 x, uint256 y) internal pure returns (uint256 z) {
    require((z = x + y) >= x, "add overflow"); }
  function safeSub(uint256 x, uint256 y) internal pure returns (uint256 z) {
    require((z = x - y) <= x, "sub wraparound"); }
  function safeMul(uint256 x, uint256 y) internal pure returns (uint256 z) {
    require(y == 0 || (z = x * y) / y == x, "mul overflow"); }
  function safeDiv(uint256 x, uint256 y) internal pure returns (uint256 z) {
    require(y != 0, "div by zero"); z = x / y; }
  function safeMod(uint256 x, uint256 y) internal pure returns (uint256 z) {
    require(y != 0, "div by zero"); z = x % y; }

  function unsafeAdd(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked { z = x + y; } }
  function unsafeSub(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked { z = x - y; } }
  function unsafeMul(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked { z = x * y; } }
  function unsafeDiv(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked { z = x / y; } }
  function unsafeMod(uint256 x, uint256 y) internal pure returns (uint256 z) {
    unchecked { z = x % y; } }

  function safeSqrt(uint256 y) internal pure returns (uint256 z) {
    if (y > 3) {
      z = y;
      uint256 x = y / 2 + 1;
      while (x < z) {
        z = x;
        x = (y / x + x) / 2;
      }
    } else if (y != 0) {
      z = 1;
    }
  }

  function reachRequire(bool succ, uint256 errMsg) internal pure {
    if ( ! succ ) {
      revert ReachError(errMsg);
    }
  }

  function checkFunReturn(bool succ, bytes memory returnData, uint256 errMsg) internal pure returns (bytes memory) {
    if (succ) {
      return returnData;
    } else {
      if (returnData.length > 0) {
        assembly {
          let returnData_size := mload(returnData)
          revert(add(32, returnData), returnData_size)
        }
      } else {
        revert ReachError(errMsg);
      }
    }
  }

  function tokenAllowance(address payable token, address owner, address spender) internal returns (uint256 amt) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(IERC20.allowance.selector, owner, spender));
    checkFunReturn(ok, ret, 0 /*'token.allowance'*/);
    amt = abi.decode(ret, (uint256));
  }

  function tokenTransferFrom(address payable token, address sender, address recipient, uint256 amt) internal returns (bool res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(IERC20.transferFrom.selector, sender, recipient, amt));
    checkFunReturn(ok, ret, 1 /*'token.transferFrom'*/);
    res = abi.decode(ret, (bool));
  }

  function tokenTransfer(address payable token, address recipient, uint256 amt) internal returns (bool res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(IERC20.transfer.selector, recipient, amt));
    checkFunReturn(ok, ret, 2 /*'token.transfer'*/);
    res = abi.decode(ret, (bool));
  }
  function safeTokenTransfer(address payable token, address recipient, uint256 amt) internal {
    require(tokenTransfer(token, recipient, amt));
  }

  function reachTokenBurn(address payable token, uint256 amt) internal returns (bool res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(ReachToken.burn.selector, amt));
    checkFunReturn(ok, ret, 3 /*'token.burn'*/);
    res = abi.decode(ret, (bool));
  }
  function safeReachTokenBurn(address payable token, uint256 amt) internal {
    require(reachTokenBurn(token, amt));
  }

  function reachTokenDestroy(address payable token) internal returns (bool res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(ReachToken.destroy.selector));
    checkFunReturn(ok, ret, 4 /*'token.destroy'*/);
    res = true;
  }
  function safeReachTokenDestroy(address payable token) internal {
    require(reachTokenDestroy(token));
  }

  function readPayAmt(address sender, address payable token) internal returns (uint256 amt) {
    amt = tokenAllowance(token, sender, address(this));
    require(checkPayAmt(sender, token, amt));
  }

  function checkPayAmt(address sender, address payable token, uint256 amt) internal returns (bool) {
    return tokenTransferFrom(token, sender, address(this), amt);
  }

  function tokenApprove(address payable token, address spender, uint256 amt) internal returns (bool res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0)}(abi.encodeWithSelector(IERC20.approve.selector, spender, amt));
    checkFunReturn(ok, ret, 5 /*'token.approve'*/);
    res = abi.decode(ret, (bool));
  }

  function tokenBalanceOf(address payable token, address owner) internal returns (uint256 res) {
    (bool ok, bytes memory ret) = token.call{value: uint256(0) }(abi.encodeWithSelector(IERC20.balanceOf.selector, owner));
    checkFunReturn(ok, ret, 6 /*'token.balanceOf'*/);
    res = abi.decode(ret, (uint256));
  }
}

struct T0 {
  bytes32 elem0;
  bytes32 elem1;
  bytes32 elem2;
  bytes32 elem3;
  }
enum _enum_T1 {None, Some}
struct T1 {
  _enum_T1 which;
  bool _None;
  T0 _Some;
  }

struct T2 {
  uint256 elem0;
  }
struct T3 {
  address payable v328;
  }
struct T4 {
  address payable v328;
  T0 v334;
  }
struct T5 {
  address payable v328;
  T0 v334;
  uint256 v397;
  }
struct T6 {
  address payable v328;
  T0 v334;
  uint256 v356;
  }
struct T8 {
  uint256 time;
  bool msg;
  }
struct T9 {
  T0 v334;
  uint256 v335;
  }
struct T10 {
  uint256 time;
  T9 msg;
  }
struct T11 {
  bool v348;
  uint256 v349;
  uint256 v356;
  }
struct T12 {
  T4 svs;
  T11 msg;
  }
struct T13 {
  bool v389;
  uint256 v390;
  uint256 v397;
  }
struct T14 {
  T4 svs;
  T13 msg;
  }
struct T15 {
  uint256 elem0;
  address payable elem1;
  }
enum _enum_T16 {verifierAPI_insert_money0_138, verifierAPI_verify0_138}
struct T16 {
  _enum_T16 which;
  T2 _verifierAPI_insert_money0_138;
  T15 _verifierAPI_verify0_138;
  }

struct T17 {
  T16 v431;
  }
struct T18 {
  uint256 time;
  T17 msg;
  }
struct T19 {
  T0 elem0;
  uint256 elem1;
  }
struct T20 {
  T19 v370;
  }
struct T21 {
  uint256 time;
  T20 msg;
  }


contract ReachContract is Stdlib {
  uint256 current_step;
  uint256 current_time;
    bytes current_svbs;
  uint256 creation_time;
  function _reachCreationTime() external view returns (uint256) { return creation_time; }
  function _reachCurrentTime() external view returns (uint256) { return current_time; }
  function _reachCurrentState() external view returns (uint256, bytes memory) { return (current_step, current_svbs); }
  mapping (uint256 => T1) map0;
  function __reachMap0Ref(uint256 addr)  internal view returns (T1 memory res) {
    if (map0[addr].which == _enum_T1.Some) {
      res = map0[addr];}
    else {
      res.which = _enum_T1.None;
      res._None = false;
      }}
  function _reachMap0Ref(uint256 addr)  external view returns (T1 memory res) {
    res = __reachMap0Ref(addr);}
  
  
  
  
  
  function views_retrieve_results_wrapped(T2 memory _a)  internal view returns (T0 memory _viewRet) {
    if (current_step == uint256(1)) {
      (T3 memory vvs) = abi.decode(current_svbs, (T3));
      reachRequire((false), uint256(7) /*'invalid view_i'*/);
      }
    if (current_step == uint256(2)) {
      (T4 memory vvs) = abi.decode(current_svbs, (T4));
      reachRequire((false), uint256(7) /*'invalid view_i'*/);
      }
    if (current_step == uint256(6)) {
      (T5 memory vvs) = abi.decode(current_svbs, (T5));
      
      
      return (((__reachMap0Ref(_a.elem0)).which == _enum_T1.Some ? (__reachMap0Ref(_a.elem0))._Some : vvs.v334));
      
      
      }
    if (current_step == uint256(7)) {
      (T6 memory vvs) = abi.decode(current_svbs, (T6));
      
      
      return (((__reachMap0Ref(_a.elem0)).which == _enum_T1.Some ? (__reachMap0Ref(_a.elem0))._Some : vvs.v334));
      
      
      }
    reachRequire((false), uint256(7) /*'invalid view_i'*/);
    }
  function views_retrieve_results(uint256 v859)  external view returns (T0 memory) {
    T2 memory _t;
    _t.elem0 = v859;
    return views_retrieve_results_wrapped(_t);
    }
  
  
  
  
  struct ApiRng {
    T0 attacherAPI_insert_position;
    uint256 verifierAPI_insert_money;
    bool verifierAPI_verify;
    }
  event _reach_oe_v374(T0 v0);
  event _reach_oe_v439(uint256 v0);
  event _reach_oe_v524(bool v0);
  event _reach_oe_v532(bool v0);
  event _reach_oe_v540(bool v0);
  
  
  event _reach_e0(address _who, T8 _a);
  
  constructor(T8 memory _a) payable {
    current_step = 0x0;
    creation_time = uint256(block.number);
    
    
    emit _reach_e0(msg.sender, _a);
    reachRequire((msg.value == uint256(0)), uint256(8) /*'(./index.rsh:67:11:dot,[],"verify network token pay amount")'*/);
    T3 memory nsvs;
    nsvs.v328 = payable(msg.sender);
    current_step = uint256(1);
    current_time = uint256(block.number);
    current_svbs = abi.encode(nsvs);
    
    
    }
  
  event _reach_e1(address _who, T10 _a);
  
  function _reach_m1(T10 calldata _a) external payable {
    ApiRng memory _r;
    _reach_m1(_a, _r);
    }
  function _reach_m1(T10 memory _a, ApiRng memory _apiRet)  internal  {
    reachRequire((current_step == uint256(1)), uint256(11) /*'state step check at ./index.rsh:76:11:dot'*/);
    reachRequire(((_a.time == uint256(0)) || (current_time == _a.time)), uint256(12) /*'state time check at ./index.rsh:76:11:dot'*/);
    current_step = 0x0;
    (T3 memory _svs) = abi.decode(current_svbs, (T3));
    
    
    emit _reach_e1(msg.sender, _a);
    reachRequire((msg.value == uint256(0)), uint256(9) /*'(./index.rsh:76:11:dot,[],"verify network token pay amount")'*/);
    reachRequire(((_svs.v328 == payable(msg.sender))), uint256(10) /*'(./index.rsh:76:11:dot,[],Just "sender correct")'*/);
    map0[_a.msg.v335].which = _enum_T1.Some;
    map0[_a.msg.v335]._Some = _a.msg.v334;
    
    T4 memory nsvs;
    nsvs.v328 = _svs.v328;
    nsvs.v334 = _a.msg.v334;
    current_step = uint256(2);
    current_time = uint256(block.number);
    current_svbs = abi.encode(nsvs);
    
    
    }
  
  event _reach_e2(address _who, T8 _a);
  
  function _reach_m2(T8 calldata _a) external payable {
    ApiRng memory _r;
    _reach_m2(_a, _r);
    }
  function _reach_m2(T8 memory _a, ApiRng memory _apiRet)  internal  {
    reachRequire((current_step == uint256(2)), uint256(15) /*'state step check at ./index.rsh:81:11:dot'*/);
    reachRequire(((_a.time == uint256(0)) || (current_time == _a.time)), uint256(16) /*'state time check at ./index.rsh:81:11:dot'*/);
    current_step = 0x0;
    (T4 memory _svs) = abi.decode(current_svbs, (T4));
    
    
    emit _reach_e2(msg.sender, _a);
    reachRequire((msg.value == uint256(0)), uint256(13) /*'(./index.rsh:81:11:dot,[],"verify network token pay amount")'*/);
    reachRequire(((_svs.v328 == payable(msg.sender))), uint256(14) /*'(./index.rsh:81:11:dot,[],Just "sender correct")'*/);
    T12 memory la;
    la.svs.v328 = _svs.v328;
    la.svs.v334 = _svs.v334;
    la.msg.v348 = true;
    la.msg.v349 = uint256(block.number);
    la.msg.v356 = uint256(0);
    l3(la);
    
    
    }
  
  
  function l3(T12 memory _a)  internal {
    
    
    if (_a.msg.v348) {
      T6 memory nsvs;
      nsvs.v328 = _a.svs.v328;
      nsvs.v334 = _a.svs.v334;
      nsvs.v356 = _a.msg.v356;
      current_step = uint256(7);
      current_time = uint256(block.number);
      current_svbs = abi.encode(nsvs);
      }
    else {
      T14 memory la;
      la.svs.v328 = _a.svs.v328;
      la.svs.v334 = _a.svs.v334;
      la.msg.v389 = true;
      la.msg.v390 = _a.msg.v349;
      la.msg.v397 = _a.msg.v356;
      l4(la);
      }
    
    }
  
  
  function l4(T14 memory _a)  internal {
    
    
    if (_a.msg.v389) {
      T5 memory nsvs;
      nsvs.v328 = _a.svs.v328;
      nsvs.v334 = _a.svs.v334;
      nsvs.v397 = _a.msg.v397;
      current_step = uint256(6);
      current_time = uint256(block.number);
      current_svbs = abi.encode(nsvs);
      }
    else {
      _a.svs.v328.transfer(_a.msg.v397);
      current_step = 0x0;
      current_time = 0x0;
      delete current_svbs;
      }
    
    }
  
  event _reach_e5(address _who, T18 _a);
  struct _F5 {
    T2 v434;
    T15 v491;
    }
  function _reach_m5(T18 calldata _a) external payable {
    ApiRng memory _r;
    _reach_m5(_a, _r);
    }
  function _reach_m5(T18 memory _a, ApiRng memory _apiRet)  internal  {
    reachRequire((current_step == uint256(6)), uint256(19) /*'state step check at ./index.rsh:130:19:dot'*/);
    reachRequire(((_a.time == uint256(0)) || (current_time == _a.time)), uint256(20) /*'state time check at ./index.rsh:130:19:dot'*/);
    current_step = 0x0;
    (T5 memory _svs) = abi.decode(current_svbs, (T5));
    _F5 memory _f;
    
    emit _reach_e5(msg.sender, _a);
    if (_a.msg.v431.which == _enum_T16.verifierAPI_insert_money0_138) {
      _f.v434 = _a.msg.v431._verifierAPI_insert_money0_138;
      reachRequire((msg.value == (_f.v434.elem0)), uint256(17) /*'(./index.rsh:130:19:dot,[],"verify network token pay amount")'*/);
      emit _reach_oe_v439( (_f.v434.elem0));
      _apiRet.verifierAPI_insert_money = (_f.v434.elem0);
      
      T14 memory la;
      la.svs.v328 = _svs.v328;
      la.svs.v334 = _svs.v334;
      la.msg.v389 = true;
      la.msg.v390 = uint256(block.number);
      la.msg.v397 = (safeAdd(_svs.v397, (_f.v434.elem0)));
      l4(la);
      
      }
    else {
      if (_a.msg.v431.which == _enum_T16.verifierAPI_verify0_138) {
        _f.v491 = _a.msg.v431._verifierAPI_verify0_138;
        reachRequire((msg.value == uint256(0)), uint256(18) /*'(./index.rsh:130:19:dot,[],"verify network token pay amount")'*/);
        if ((_svs.v397 >= uint256(1000000000000000000))) {
          (_f.v491.elem1).transfer(uint256(1000000000000000000));
          emit _reach_oe_v524( (true));
          _apiRet.verifierAPI_verify = (true);
          
          emit _reach_oe_v532( (false));
          _apiRet.verifierAPI_verify = (false);
          
          delete map0[(_f.v491.elem0)];
          T14 memory la;
          la.svs.v328 = _svs.v328;
          la.svs.v334 = _svs.v334;
          la.msg.v389 = false;
          la.msg.v390 = uint256(block.number);
          la.msg.v397 = (safeSub(_svs.v397, uint256(1000000000000000000)));
          l4(la);
          }
        else {
          emit _reach_oe_v540( (false));
          _apiRet.verifierAPI_verify = (false);
          
          delete map0[(_f.v491.elem0)];
          T14 memory la;
          la.svs.v328 = _svs.v328;
          la.svs.v334 = _svs.v334;
          la.msg.v389 = false;
          la.msg.v390 = uint256(block.number);
          la.msg.v397 = _svs.v397;
          l4(la);
          }
        }
      else {
        }}
    
    }
  
  event _reach_e6(address _who, T21 _a);
  
  function _reach_m6(T21 calldata _a) external payable {
    ApiRng memory _r;
    _reach_m6(_a, _r);
    }
  function _reach_m6(T21 memory _a, ApiRng memory _apiRet)  internal  {
    reachRequire((current_step == uint256(7)), uint256(22) /*'state step check at ./index.rsh:92:17:dot'*/);
    reachRequire(((_a.time == uint256(0)) || (current_time == _a.time)), uint256(23) /*'state time check at ./index.rsh:92:17:dot'*/);
    current_step = 0x0;
    (T6 memory _svs) = abi.decode(current_svbs, (T6));
    
    
    emit _reach_e6(msg.sender, _a);
    reachRequire((msg.value == uint256(0)), uint256(21) /*'(./index.rsh:92:17:dot,[],"verify network token pay amount")'*/);
    emit _reach_oe_v374( (_a.msg.v370.elem0));
    _apiRet.attacherAPI_insert_position = (_a.msg.v370.elem0);
    
    T12 memory la;
    la.svs.v328 = _svs.v328;
    la.svs.v334 = _svs.v334;
    la.msg.v348 = false;
    la.msg.v349 = uint256(block.number);
    la.msg.v356 = _svs.v356;
    l3(la);
    
    
    }
  
  
  function attacherAPI_insert_position(T0 memory _a0, uint256 _a1)  external payable returns (T0  memory) {
    T21 memory _t;
    _t.msg.v370.elem0 = _a0;
    _t.msg.v370.elem1 = _a1;
    {
      ApiRng memory _r;
      _reach_m6(_t, _r);
      return _r.attacherAPI_insert_position;
      }
    }
  
  function verifierAPI_insert_money(uint256 _a0)  external payable returns (uint256 ) {
    T18 memory _t;
    _t.msg.v431.which = _enum_T16.verifierAPI_insert_money0_138;
    _t.msg.v431._verifierAPI_insert_money0_138.elem0 = _a0;
    {
      ApiRng memory _r;
      _reach_m5(_t, _r);
      return _r.verifierAPI_insert_money;
      }
    }
  
  function verifierAPI_verify(uint256 _a0, address payable _a1)  external payable returns (bool ) {
    T18 memory _t;
    _t.msg.v431.which = _enum_T16.verifierAPI_verify0_138;
    _t.msg.v431._verifierAPI_verify0_138.elem0 = _a0;
    _t.msg.v431._verifierAPI_verify0_138.elem1 = _a1;
    {
      ApiRng memory _r;
      _reach_m5(_t, _r);
      return _r.verifierAPI_verify;
      }
    }
  
  
  receive () external payable {}
  fallback () external payable {}
  
  }
